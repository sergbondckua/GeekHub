import sqlite3
import json
import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
from colorama import init, Fore, Back, Style

init(autoreset=True)  # Автоматичне додавання Style.RESET_ALL в кінець print
conn = sqlite3.connect('atm.db')


class AtmException(Exception):
    pass


def auth_validate(login: str, passwd=None) -> bool | tuple:
    """Перевіряє валідність введених даних"""
    try:
        with conn:
            cursor = conn.cursor()
            users = cursor.execute(
                """SELECT username, password FROM users""").fetchall()
            if (login, passwd) in users:
                return True

            for user in users:
                # Якщо login вірний, а пароль ні, даємо ще спроби вводу пароля
                if user[0] == login:
                    for attempt in range(3):
                        if user[1] == input(Fore.LIGHTMAGENTA_EX +
                                            "Wrong password, try again: "):
                            return True
                        else:
                            if attempt < 1:
                                print(f"Try again, {2 - attempt} attempt!")
                            elif attempt < 2:
                                print("Try again, last attempt!")
                    raise Exception("Access denied!")

        # Якщо клієнта немає в БД, пропонуємо реєстрацію
        print(Fore.LIGHTGREEN_EX + f"{login} - available for registration")
        if input("You want sign_up? - yes/no: ").strip() in ["yes", "y"]:
            return sign_up(login, passwd)
        raise Exception("Access denied, Bye!")

    except sqlite3.OperationalError as ex:
        print("[INFO] Error while working with SQLite3,", ex)
    except Exception as ex:
        print(ex)

    return False


def validate_same_password(passwd: str) -> str:
    """Перевірка на однаковість паролів"""
    password_2 = input(Fore.LIGHTMAGENTA_EX +
                       "Repeat your password: ")
    if passwd == password_2:
        return passwd
    else:
        print(Fore.RED + "Passwords don't match!")
        new_password = input(Fore.LIGHTMAGENTA_EX +
                             "Enter new password: ")
        if validate_diff_passwd(new_password):
            return validate_same_password(new_password)


def validate_diff_passwd(passwd: str) -> bool:
    """ Перевірка на складність пароля"""
    if len(passwd) < 8:
        print("Password must be longer than 7 characters")
        validate_diff_passwd(input("Input other password: "))
    elif not any([char.isdigit() for char in passwd]):
        print("Password must have at least one digit")
        validate_diff_passwd(input("Input other password: "))
    elif not any([char.isupper() for char in passwd]):
        print("Password must contain an uppercase letter")
        validate_diff_passwd(input("Input other password: "))
    return True


def sign_up(client: str, passwd: str) -> tuple:
    """Реєстрація нового клієнта"""
    print(Fore.LIGHTRED_EX + "Registration".center(100, '~'))
    with conn:
        cursor = conn.cursor()
        users = cursor.execute("SELECT username FROM users").fetchall()

        if client in [name[0] for name in users]:
            print('Name is already registered, try again with unique name')
            return sign_up(input("Input username: "), passwd)

        if validate_diff_passwd(passwd):
            password = validate_same_password(passwd)
            cursor.execute(
                """INSERT INTO users (username, password, balance, staff)
                    VALUES (?,?,?,?)""", (client, password, 0, "client")
            )
            conn.commit()
        print(Fore.GREEN + "Registered done. Wellcome to ATM!".center(100, '~'))
    return client, password


def write_statement(client: str, **kwargs):
    """Записує в файл транзакції клієнта"""

    #  Формуємо дані для виписки транзакцій
    data = {
        "id": random.randint(0, 99999999),
        "time": datetime.now().timestamp().__int__(),
        "description": kwargs["desc"],
        "amount": kwargs["amount"],
        "balance": kwargs["balance"]
    }
    data = json.dumps(data)
    with conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""INSERT INTO statement (username, orders)
                VALUES (?,?)""", (client, data))
        conn.commit()


def get_atm_balance() -> int:
    """Отримує баланс банкомату"""
    with conn:
        cursor = conn.cursor()
        query = cursor.execute("SELECT * FROM money_bills").fetchall()
        atm_balance = sum([x[0] * x[1] for x in query])
    return atm_balance


def get_balance(client: str) -> int:
    """Отримує баланс клієнта"""
    with conn:
        cursor = conn.cursor()
        balance = cursor.execute(
            "SELECT balance FROM users WHERE username = :client",
            {"client": client}).fetchone()[0]
        return balance


def get_client_balance_menu(client: str):
    balance = get_balance(client)
    print(Fore.YELLOW + f"{client.capitalize()}, "
                        f"your balance is "
                        f"{Fore.BLACK}{Back.YELLOW}${balance}"
                        f"{Style.RESET_ALL}\n")


def make_deposit(client: str) -> tuple:
    """Поповнює баланс"""
    with conn:
        cursor = conn.cursor()
        min_bill = cursor.execute(
            "SELECT MIN(bill) FROM money_bills").fetchone()[0]

        current_balance = get_balance(client)
        deposit = abs(int(input(Fore.LIGHTMAGENTA_EX +
                                "Enter your deposit: $")))
        new_balance = 0
        rest = deposit % min_bill

        if deposit >= min_bill:  # Якщо введена сума більша за мінімальну купюру
            if rest != 0:  # Якщо не кратна мінімальній купюрі
                new_balance = current_balance + deposit - rest
                deposit -= rest
                print(Fore.RED + f"Bills are not supported, refund: ${rest}")
            else:
                new_balance = current_balance + deposit
            cursor.execute(
                """UPDATE users SET balance = ?
                    WHERE username = ?""", (new_balance, client))
            conn.commit()
            write_statement(
                client, desc="Deposit", amount=deposit, balance=new_balance)
            print(Fore.LIGHTGREEN_EX +
                  f"{client.capitalize()}, "
                  f"now {Back.LIGHTBLACK_EX}+${deposit}"
                  f"{Style.RESET_ALL + Fore.LIGHTGREEN_EX} and "
                  f"your new balance is {Back.LIGHTBLACK_EX}"
                  f"🔺${new_balance}{Style.RESET_ALL}\n"
                  )
        else:
            print(Back.LIGHTRED_EX + Fore.LIGHTWHITE_EX +
                  f"Bills are not supported! Refund money: ${deposit}"
                  f"{Style.RESET_ALL}\n")
        return deposit, new_balance


def withdraw_balance(amount_funds: int) -> list:
    with conn:
        cursor = conn.cursor()
        query = cursor.execute(
            "SELECT * FROM money_bills ORDER BY bill DESC").fetchall()
        banknotes_load = {item[0]: item[1] for item in query}

    withdraw_banknotes = []
    counter = 1
    while sum(withdraw_banknotes) < amount_funds:
        stop = False
        if counter > len(banknotes_load.keys()):
            with conn:
                with conn:
                    cursor = conn.cursor()
                    min_bill = cursor.execute(
                        "SELECT MIN(bill) "
                        "FROM money_bills WHERE count > 0").fetchone()[0]
            raise AtmException(
                "There are no banknotes to issue the specified amount\n"
                f"Input positive amount which is multiple by ${min_bill}")

        for key in banknotes_load.keys():
            if stop:
                break
            elif key + sum(withdraw_banknotes) <= amount_funds and banknotes_load[key] > 0:
                for k in banknotes_load.keys():
                    if (amount_funds - sum(withdraw_banknotes) - key) % k == 0 and banknotes_load[k] > 0:
                        withdraw_banknotes.append(key)
                        banknotes_load[key] -= 1
                        stop = True
                        break
        counter += 1
    for bill, count in banknotes_load.items():
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE money_bills SET count = ? WHERE bill= ?", (count, bill)
            )
            conn.commit()
    return withdraw_banknotes


def make_withdraw(client: str) -> tuple:
    """Знімає кошти, зменшує баланс"""
    with conn:
        cursor = conn.cursor()
        min_bill = cursor.execute(
            "SELECT MIN(bill) FROM money_bills").fetchone()[0]
    amount = abs(int(input(Fore.LIGHTMAGENTA_EX +
                           "What amount to withdraw?: $")))
    current_balance = get_balance(client)
    new_balance = current_balance - amount
    atm_balance = get_atm_balance()

    if atm_balance - amount >= 0 and new_balance >= 0:
        if amount % min_bill == 0:
            try:
                print("Your banknotes:", withdraw_balance(amount))
            except AtmException as ex:
                print(ex)
                make_withdraw(client)
            else:
                with conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        """UPDATE users SET balance = ?
                                WHERE username = ?""", (new_balance, client))
                    conn.commit()
                    write_statement(
                        client,
                        desc="Withdraw",
                        amount=-amount,
                        balance=new_balance
                    )
                    print(Fore.LIGHTGREEN_EX +
                          f"{client.capitalize()}, "
                          f"now {Back.LIGHTBLACK_EX}-${amount}"
                          f"{Style.RESET_ALL + Fore.LIGHTGREEN_EX} and "
                          f"your new balance is {Back.LIGHTBLACK_EX}"
                          f"🔻${new_balance}{Style.RESET_ALL}\n")
                return amount, new_balance
        else:
            print("Input positive amount which is multiple by zero")
    else:
        print(Fore.RED + f"It is not possible to withdraw "
                         f"{Fore.BLACK}{Back.RED}${amount}{Style.RESET_ALL}"
                         f"{Fore.RED}, your balance: {Back.LIGHTWHITE_EX}"
                         f"${get_balance(client)}{Style.RESET_ALL}"
                         f"{Fore.RED}, ATM balance: {Back.LIGHTWHITE_EX}"
                         f"${atm_balance}{Style.RESET_ALL}"
              )


def get_statement(client) -> None:
    """Показує всю виписку клієнта"""
    with conn:
        cursor = conn.cursor()
        statement = cursor.execute(
            """SELECT orders FROM statement WHERE username = :client
                ORDER BY id DESC""",
            {"client": client}).fetchall()
        [print(i[0], end="\n") for i in statement]


def get_input_auth() -> tuple:
    """Повертає введені дані для авторизації"""
    username = input("Enter a username : ")
    password = input("Input password: ")
    return username, password


def close():
    """Завершення роботи програми"""
    print("Bye!")
    exit()


# Меню клієнта
def client_menu(client):
    choice = input("Select:\n"
                   "1 - Balance\n"
                   "2 - Deposit\n"
                   "3 - Withdraw\n"
                   "4 - Statement\n"
                   "5 - Log Out\n"
                   "Make your choice: ")
    choices = {
        "1": get_client_balance_menu,
        "2": make_deposit,
        "3": make_withdraw,
        "4": get_statement,
    }
    choices.get(choice, "5")(client) if choices.get(choice) else main()
    return client_menu(client)


def all_statements(client):
    with conn:
        cursor = conn.cursor()
        statement = cursor.execute(
            """SELECT * FROM statement ORDER BY id DESC """).fetchall()
        [print(i, end="\n") for i in sorted(statement, key=lambda x: x[1])]


def change_bills(login: str):
    """Change money in ATM"""
    with conn:
        cursor = conn.cursor()
        money = cursor.execute("SELECT * FROM money_bills").fetchall()
        add_money = {i[0]: i[1] for i in money}
        choice = {str(num + 1): bill[0] for num, bill in enumerate(money)}
        [print(f'press [{num}] --> 💵{bill}') for num, bill in choice.items()]
        change = input(f"What bill are we changing?: ")
        choose = choice.get(change)

        if choose in [item[0] for item in money]:
            amount = int(input("What is the amount (use '-' to reduce): "))
            result = add_money.get(choose) + amount
            if result < 0:
                print(Fore.WHITE + Back.LIGHTRED_EX +
                      f"Wrong entry, not enough ${choose} banknotes to withdraw. "
                      f"Available only: {add_money.get(choose)} pcs")
            else:
                cursor.execute(
                    "UPDATE money_bills SET count = ? WHERE bill = ?",
                    (result, choose)
                )
                conn.commit()
                write_statement(login,
                                desc="Change money",
                                amount={choose: amount},
                                balance={choose: result}
                                )
                print(Fore.BLACK + Back.LIGHTYELLOW_EX +
                      f"Banknote 💵${choose} has been changed to {amount} pcs."
                      f" Now 💵${choose} total: {result} pcs.")
        else:
            print("Not found banknote")

    return collector_menu(login)


def revision_bills(login: str):
    """Check money in ATM"""
    print(Fore.BLACK + Back.LIGHTYELLOW_EX +
          f"ATM balance: ${get_atm_balance()}{Style.RESET_ALL}\n"
          f"Content availability:")
    with conn:
        cursor = conn.cursor()
        money = cursor.execute("SELECT * FROM money_bills").fetchall()
        for item in money:
            print("💰", item[0], "⇢", item[1], "pcs")
    return collector_menu(login)


# Меню інкасатора
def collector_menu(client):
    choice = input("Select:\n"
                   "1 - Balance\n"
                   "2 - Change Banknotes\n"
                   "3 - Statement\n"
                   "4 - Log Out\n"
                   "Make your choice: ")
    choices = {
        "1": revision_bills,
        "2": change_bills,
        "3": all_statements,
    }
    choices.get(choice, "4")(client) if choices.get(choice) else main()
    return collector_menu(client)


# Test plot
def show_plot(client):
    with conn:
        cursor = conn.cursor()
        statement = cursor.execute(
            """SELECT orders FROM statement WHERE username = :client
                ORDER BY id DESC""",
            {"client": client}).fetchall()
        total = [json.loads(i[0]) for i in statement]
        plus = sorted([item["amount"] for item in total if item["description"] == "Deposit"], reverse=True)
        minus = sorted([item["amount"] for item in total if item["description"] == "Withdraw"], reverse=True)
        data = {"withdraw": minus}
        df = pd.DataFrame(data)
        x = np.arange(len(minus))
        plt.axis([0, len(minus), 0, 1000 if not minus else max(minus)])
        plt.plot(x, df)
        plt.legend(data, loc=1)
        plt.show()


def main():
    # Головне МЕНЮ
    username = ""
    password = ""
    choice = input("MENU:\n"
                   "1 - Sign In\n"
                   "2 - Sign Up\n"
                   "3 - Exit\n"
                   "Make your choice: ")
    if choice == "1":
        username, password = get_input_auth()
    elif choice == "2":
        auth = get_input_auth()
        username, password = sign_up(auth[0], auth[1])
    else:
        close()

    # Доступ після успішної авторизації
    if auth_validate(username, password):
        with conn:
            cursor = conn.cursor()
            staff = cursor.execute(
                "SELECT staff FROM users WHERE username = :client",
                {"client": username}).fetchone()[0]

            if staff == "collector":
                collector_menu(username)

        print(
            Fore.CYAN + f"\nHello {username.capitalize()}, "
                        f"access successfully\n" + Style.RESET_ALL
        )
        client_menu(username)


if __name__ == '__main__':
    main()
    # make_withdraw('user1')
    # show_plot('user1')
