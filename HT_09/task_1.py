"""Банкомат 2.0"""

import sqlite3
import json
import random
from datetime import datetime
from colorama import init, Fore, Back, Style

init(autoreset=True)  # Автоматичне додавання Style.RESET_ALL в кінець print
conn = sqlite3.connect('atm.db')


def auth_validate(login: str, passwd=None) -> bool:
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
                                            "Input password: "):
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
            return sign_up(login)
        raise Exception("Access denied, Bye!")

    except sqlite3.OperationalError as ex:
        print("[INFO] Error while working with SQLite3,", ex)
    except Exception as ex:
        print(ex)

    return False


def password_validate(client: str) -> str:
    """Checks the match passwords"""
    password_1 = input(Fore.LIGHTMAGENTA_EX +
                       f"Enter your new password for {client}: ")
    password_2 = input(Fore.LIGHTMAGENTA_EX +
                       "Repeat your password: ")
    if password_1 == password_2:
        return password_1
    else:
        print(Fore.RED + "Passwords don't match!")
        return password_validate(client)


def close(client: str):
    """Завершення роботи програми"""
    print(client + ", Bye!")
    exit()


def sign_up(client: str):
    """Реєстрація нового клієнта"""
    print(Fore.LIGHTRED_EX + "Registration".center(100, '~'))
    with conn:
        cursor = conn.cursor()
        users = cursor.execute("SELECT username FROM users").fetchall()

        if client in [name[0] for name in users]:
            print('Name is already registered, try again with unique name')
            return sign_up(input("Input username: "))

        passwd = password_validate(client)
        cursor.execute(
            """INSERT INTO users (username, password, balance, staff)
                VALUES (?,?,?,?)""", (client, passwd, 0, "client")
        )
        conn.commit()
    print(Fore.GREEN + "Registered done. Wellcome to ATM!".center(100, '~'))
    return auth_validate(client, passwd)


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
            {"client": client}).fetchone()
        print(Fore.YELLOW + f"{client.capitalize()}, "
                            f"your balance is "
                            f"{Fore.BLACK}{Back.YELLOW}${balance[0]}"
                            f"{Style.RESET_ALL}\n")
        return balance[0]


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
                f"""UPDATE users SET balance = ?
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


def make_withdraw(client: str) -> tuple:
    """Знімає кошти, зменшує баланс"""
    amount = abs(int(input(Fore.LIGHTMAGENTA_EX +
                           "What amount to withdraw?: $")))
    current_balance = get_balance(client)
    new_balance = current_balance - amount
    atm_balance = get_atm_balance()

    if new_balance >= 0 and atm_balance - amount >= 0:
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                f"""UPDATE users SET balance = ?
                    WHERE username = ?""", (new_balance, client))
            conn.commit()
            write_statement(client, desc="Withdraw", amount=-amount, balance=new_balance)
            print(Fore.LIGHTGREEN_EX +
                  f"{client.capitalize()}, "
                  f"now {Back.LIGHTBLACK_EX}-${amount}"
                  f"{Style.RESET_ALL + Fore.LIGHTGREEN_EX} and "
                  f"your new balance is {Back.LIGHTBLACK_EX}"
                  f"🔻${new_balance}{Style.RESET_ALL}\n")
            return amount, new_balance
    else:
        print(Fore.RED + f"It is not possible to withdraw "
                         f"{Fore.BLACK}{Back.RED}${amount}{Style.RESET_ALL}"
                         f"{Fore.RED}, your balance: {Back.LIGHTWHITE_EX}"
                         f"${get_balance(client)}{Style.RESET_ALL}"
                         f"{Fore.RED}, ATM balance: {Back.LIGHTWHITE_EX}"
                         f"${atm_balance}{Style.RESET_ALL}"
              )


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

    return staff_menu(login)


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
    return staff_menu(login)


def staff_menu(login: str):
    choice = input(Fore.LIGHTYELLOW_EX + "Select:\n"
                                         "1️⃣ - ➕Change money\n"
                                         "2️⃣ - 💱Revision money\n"
                                         "3️⃣ - ❌EXIT\n"
                   )
    choices = {
        "1": change_bills,
        "2": revision_bills,
        "3": close,
    }
    return choices.get(choice, close)(login)


def main():
    print(Fore.CYAN + "Authorization required: Sign in or Sign up please!")
    username = input(Fore.LIGHTMAGENTA_EX +
                     "Enter a username to sign in or register: ")
    run = True

    if auth_validate(username):
        with conn:
            cursor = conn.cursor()
            staff = cursor.execute(
                "SELECT staff FROM users WHERE username = :client",
                {"client": username}).fetchone()
            if staff[0] == "collector":
                staff_menu(username)
        print(
            Fore.CYAN + f"\nHello {username.capitalize()}, "
                        f"access successfully\n" + Style.RESET_ALL
        )
        while run:
            choose = input(Fore.LIGHTBLACK_EX +
                           f"CHOOSE AN ITEM:{Style.RESET_ALL}\n"
                           f"{Fore.LIGHTYELLOW_EX}1️⃣ - 📊Balance{Style.RESET_ALL}\n"
                           f"{Fore.GREEN}2️⃣ - 🔺Deposit{Style.RESET_ALL}\n"
                           f"{Fore.MAGENTA}3️⃣ - 🔻Withdraw{Style.RESET_ALL}"
                           f"{Fore.RESET}\n4️⃣ - ❌EXIT\n" + Style.RESET_ALL
                           )
            # Select 1
            if choose == "1":
                print(f"[BALANCE]".center(30, "#"))
                get_balance(username)

            # Select 2
            elif choose == "2":
                print("[DEPOSIT]".center(30, "#"))
                make_deposit(username)

            # Select 3
            elif choose == "3":
                print("[WITHDRAW]".center(30, "#"))
                make_withdraw(username)

            # Select 4
            elif choose == "4":
                print("[EXIT]".center(30, "#"))
                print(f"Bye-bye, {username.capitalize()}!".center(30, '-'))
                run = False
                conn.close()
            else:
                print(Fore.YELLOW +
                      "Such an item is not on the menu. Try again!\n"
                      )


if __name__ == '__main__':
    main()
