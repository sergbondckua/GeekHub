"""
Банкомат 4.0
"""

import sqlite3
import json
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from colorama import init, Fore, Back, Style

init(autoreset=True)  # Автоматичне додавання Style.RESET_ALL в кінець print
conn = sqlite3.connect('atm.db')  # з'єднання з БД


class AtmException(Exception):
    pass


class Client:
    """Опції клієнта"""
    conn = sqlite3.connect('atm.db')  # з'єднання з БД
    with conn:
        cursor = conn.cursor()  # створюємо курсор

    def __init__(self, username):
        self.user = self.cursor.execute(
            """SELECT * FROM users WHERE username = ?""",
            (username,)).fetchone()
        self.login = self.user[1]
        self.password = self.user[2]
        self.balance = self.user[3]
        self.staff = self.user[4]

    def get_balance(self) -> int:
        """Показує баланс клієнта"""
        return int(self.balance)

    def change_balance(self, new_balance):
        """Оновлює баланс клієнта в БД"""
        self.cursor.execute(
            """UPDATE users SET balance = ?
                WHERE username = ?""", (new_balance, self.login))
        self.conn.commit()

    def get_statement(self) -> list:
        """Виписка транзакцій клієнта"""
        return self.cursor.execute(
            """SELECT orders FROM statement WHERE username = ?
                ORDER BY id DESC""",
            (self.login,)).fetchall()


class Atm:
    """Опції банкомату"""
    conn = sqlite3.connect('atm.db')  # з'єднання з БД
    with conn:
        cursor = conn.cursor()  # створюємо курсор

    def get_atm_balance(self) -> int:
        """Отримує баланс банкомату"""
        query = self.cursor.execute(
            "SELECT * FROM money_bills ORDER BY bill DESC").fetchall()
        return sum([x[0] * x[1] for x in query])

    def all_nominal(self) -> list:
        """Повертає список номінальних банкнот"""
        query = self.cursor.execute(
            "SELECT * FROM money_bills ORDER BY bill DESC").fetchall()
        return [i[0] for i in query for _ in range(i[1])]

    def dict_nominal(self) -> dict:
        query = self.cursor.execute(
            "SELECT * FROM money_bills ORDER BY bill DESC").fetchall()
        return {i[0]: i[1] for i in query}

    def min_banknotes(self) -> int:
        return self.cursor.execute(
            "SELECT MIN(bill) FROM money_bills").fetchone()[0]

    def get_all_statements(self) -> list:
        return self.cursor.execute(
            """SELECT * FROM statement ORDER BY id DESC """).fetchall()


def auth_validate(login: str) -> bool | None:
    """Перевіряє валідність введених даних"""
    user = Client(login)
    for attempt in range(3):
        if user.password == input(
                f"Input your password, you have {3 - attempt} attempts "):
            return True
        else:
            if attempt != 2:
                print(
                    f"Wrong password, try again, have {2 - attempt} attempts ")
            else:
                print('Too many attempts')
                return close()
    return False


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


def close():
    """Завершення роботи програми"""
    print("Bye!")
    exit()


def validate_same_password(passwd: str) -> str:
    """Перевірка на однаковість паролів"""
    password_2 = input(Fore.LIGHTMAGENTA_EX +
                       "Repeat your password: ").strip()
    if passwd == password_2:
        return passwd
    else:
        print(Fore.RED + "Passwords don't match!")
        while True:
            new_password = input(Fore.LIGHTMAGENTA_EX +
                                 "Enter new password: ").strip()
            if validate_diff_passwd(new_password):
                break
        return validate_same_password(new_password)


def validate_diff_passwd(passwd: str):
    """ Перевірка на складність пароля"""
    if len(passwd) < 8:
        print("Password must be longer than 7 characters")
        return False
    elif not any([char.isdigit() for char in passwd]):
        print("Password must have at least one digit")
        return False
    elif not any([char.isupper() for char in passwd]):
        print("Password must contain an uppercase letter")
        return False
    return True


def sign_up():
    """Реєстрація нового клієнта"""
    print(Fore.LIGHTRED_EX + "Registration".center(100, '~'))
    with conn:
        cursor = conn.cursor()
        users = cursor.execute("SELECT username FROM users").fetchall()

    client = input("Input username: ").strip()
    if client in [name[0] for name in users]:
        print('Name is already registered, try again with unique name')
        return sign_up()

    while True:
        passwd = input(Fore.LIGHTMAGENTA_EX + "Enter password: ").strip()
        if validate_diff_passwd(passwd):
            break

    password = validate_same_password(passwd)
    # Шанс 10% на баланс в $100
    bonus = 100 if random.random() < 0.1 else 0
    with conn:
        cursor.execute(
            """INSERT INTO users (username, password, balance, staff)
                VALUES (?,?,?,?)""", (client, password, bonus, "client")
        )
        conn.commit()
    print(Fore.GREEN +
          "Registered done. Wellcome to ATM!".center(100, '~'))
    return client_menu(client)


def get_client_balance_menu(client: str):
    balance = Client(client).get_balance()
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

        current_balance = Client(client).get_balance()
        deposit = abs(int(input(Fore.LIGHTMAGENTA_EX +
                                "Enter your deposit: $").strip()))
        new_balance = 0
        rest = deposit % min_bill

        if deposit >= min_bill:  # Якщо введена сума більша за мінімальну купюру
            if rest != 0:  # Якщо не кратна мінімальній купюрі
                new_balance = current_balance + deposit - rest
                deposit -= rest
                print(Fore.RED + f"Bills are not supported, refund: ${rest}")
            else:
                new_balance = current_balance + deposit

            Client(client).change_balance(new_balance)
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
    """Оновлює кількість номіналів купюр"""

    with conn:
        cursor = conn.cursor()
    # список всіх купюр із банкомата
    kit = Atm().all_nominal()
    sums = {0: 0}

    for i in range(1, len(kit)):
        value = kit[i - 1]  # номінал додаваної купюри
        new_sums = {}  # зберігає нові суми, при додаванні поточної купюри value
        for suma in sums.keys():
            new_sum = suma + value
            if new_sum > amount_funds:
                continue
            elif new_sum not in sums.keys():
                new_sums[new_sum] = value
        sums = sums | new_sums  # додаєм (об'єднуємо) значення
        if amount_funds in sums.keys():
            break  # одержали потрібну суму

    withdraw_banknotes = []
    if amount_funds not in sums.keys():
        raise AtmException(
            "There are no banknotes to issue the specified amount\n")
    else:
        rem = amount_funds
        while rem > 0:
            withdraw_banknotes.append(sums[rem])
            rem -= sums[rem]

    # словник всіх значень номіналів купюр із БД
    db_upload = Atm().dict_nominal()

    # формуємо словник з кількістю номіналів купюр
    db_out = {i: withdraw_banknotes.count(i) for i in withdraw_banknotes}

    # віднімаємо видані купюри
    for key, value in db_out.items():
        db_upload[key] -= value

    # Оновлюємо БД з новим залишком
    for bill, count in db_upload.items():
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE money_bills SET count = ? WHERE bill= ?", (count, bill)
            )
        conn.commit()
    return withdraw_banknotes


def make_withdraw(client: str) -> tuple:
    """Знімає кошти, зменшує баланс"""

    min_bill = Atm().min_banknotes()  # мінімальний номінал з АТМ
    amount = abs(int(input(Fore.LIGHTMAGENTA_EX +
                           "What amount to withdraw?: $").strip()))
    current_balance = Client(client).get_balance()
    new_balance = current_balance - amount
    atm_balance = Atm().get_atm_balance()

    if atm_balance - amount >= 0 and new_balance >= 0:
        if amount % min_bill == 0:
            try:
                print("Your banknotes:", withdraw_balance(amount))
            except AtmException as ex:
                print(ex)
                make_withdraw(client)
            else:
                Client(client).change_balance(new_balance)
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
                         f"${Client(client).get_balance()}{Style.RESET_ALL}"
                         f"{Fore.RED}, ATM balance: {Back.LIGHTWHITE_EX}"
                         f"${atm_balance}{Style.RESET_ALL}"
              )


def get_statement(client):
    return [print(i[0], end="\n") for i in Client(client).get_statement()]


# Меню клієнта
def client_menu(client):
    choice = input("Select:\n"
                   "1️⃣ - Balance\n"
                   "2️⃣ - Deposit\n"
                   "3️⃣ - Withdraw\n"
                   "4️⃣ - Statement\n"
                   "5️⃣ - Deposit chart\n"
                   "6️⃣ - Log Out\n"
                   "Make your choice: ")
    choices = {
        "1": get_client_balance_menu,
        "2": make_deposit,
        "3": make_withdraw,
        "4": get_statement,
        "5": show_plot
    }
    choices.get(choice, "6")(client) if choices.get(choice) else main()
    return client_menu(client)


def show_plot(client: str):
    """Показує графік поповнень рахунку"""

    statement = Client(client).get_statement()
    total = [json.loads(i[0]) for i in statement]
    plus = [i["amount"] for i in total if i["description"] == "Deposit"][::-1]

    if plus:
        data = {"Deposit": plus}
        df = pd.DataFrame(data)
        x = np.arange(len(plus))
        plt.axis([0, len(plus), 1, 1000 if not plus else max(plus)])
        plt.plot(x, df)
        plt.legend(data, loc=1)
        plt.show()
    else:
        print("No deposits found. "
              "Multiple deposits are required to display the chart")
    return client_menu(client)


def revision_bills(login: str):
    """Check money in ATM"""
    print(Fore.BLACK + Back.LIGHTYELLOW_EX +
          f"ATM balance: ${Atm().get_atm_balance()}{Style.RESET_ALL}\n"
          f"Content availability:")
    for bill, count in Atm().dict_nominal().items():
        print("💰", bill, "⇢", count, "pcs")
    return collector_menu(login)


def change_bills(login: str):
    """Change money in ATM"""

    add_money = Atm().dict_nominal()
    choice = {str(num + 1): bill for num, bill in enumerate(add_money.keys())}
    [print(f'press [{num}] --> 💵{bill}') for num, bill in choice.items()]
    change = input(f"What bill are we changing?: ").strip()
    choose = choice.get(change)

    if choose in add_money.keys():
        amount = int(input(
            "What is the amount (use '-' to reduce): ").strip())
        result = add_money.get(choose) + amount
        if result < 0:
            print(Fore.WHITE + Back.LIGHTRED_EX +
                  f"Wrong entry, not enough ${choose} banknotes to withdraw. "
                  f"Available only: {add_money.get(choose)} pcs")
        else:
            # Оновлюємо результат в БД
            with conn:
                cursor = conn.cursor()
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


def all_statements(client):
    with conn:
        cursor = conn.cursor()
        statement = Atm().get_all_statements(client)
        [print(i, end="\n") for i in sorted(statement, key=lambda x: x[1])]


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


def main():
    # Головне МЕНЮ
    choice = input("MENU:\n"
                   "1 - Sign In\n"
                   "2 - Sign Up\n"
                   "3 - Exit\n"
                   "Make your choice: ").strip()
    if choice == "1":
        login = input('Please input your login: ')
        try:
            Client(login)
        except Exception:
            if input(
                    "User not found\n"
                    "You want Sign up? - yes/no: ").strip() in ["yes", "y"]:
                sign_up()
            else:
                close()
        else:
            user = Client(login)
            user_status = user.staff
            if user_status == 'client':
                if auth_validate(login):
                    client_menu(login)
            if user_status == 'collector':
                if auth_validate(login):
                    collector_menu(login)

    elif choice == "2":
        sign_up()
    else:
        print("Access denied!")
        close()


if __name__ == '__main__':
    main()

