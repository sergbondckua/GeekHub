"""Банкомат 3.0"""

import sqlite3
import json
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from colorama import init, Fore, Back, Style

init(autoreset=True)  # Автоматичне додавання Style.RESET_ALL в кінець print


# conn = sqlite3.connect('atm.db')


class AtmException(Exception):
    pass


class Atm:
    conn = sqlite3.connect('atm.db')
    with conn:
        cursor = conn.cursor()

    def __init__(self, login=None, passwd=None):
        self.login = login
        self.password = passwd

    def auth_validate(self) -> bool:
        """Перевіряє валідність введених даних"""
        users = self.cursor.execute(
            """SELECT username, password FROM users""").fetchall()
        if (self.login, self.password) in users:
            return True
        return False

    def write_statement(self, **kwargs):
        """Записує транзакції користувачів банкомату"""

        #  Формуємо дані для виписки транзакцій
        data = {
            "id": random.randint(0, 99999999),
            "time": datetime.now().timestamp().__int__(),
            "description": kwargs["desc"],
            "amount": kwargs["amount"],
            "balance": kwargs["balance"]
        }
        data = json.dumps(data)
        with self.conn:
            # cursor = conn.cursor()
            self.cursor.execute(
                f"""INSERT INTO statement (username, orders)
                    VALUES (?,?)""", (self.login, data))
        self.conn.commit()

    def access_level(self) -> str:
        """Повертає права доступу користувача"""
        return self.cursor.execute(
            """SELECT staff FROM users WHERE username = ?""",
            (self.login,)).fetchone()[0]

    def get_user_balance(self) -> int:
        """Повертає баланс клієнта"""
        return self.cursor.execute(
            "SELECT balance FROM users WHERE username = ?",
            (self.login,)).fetchone()[0]

    def change_user_balance(self, new_balance):
        """Оновлює баланс клієнта в БД"""
        with self.conn:
            self.cursor.execute(
                """UPDATE users SET balance = ?
                    WHERE username = ?""", (new_balance, self.login))
        self.conn.commit()

    def get_atm_balance(self) -> int:
        """Повертає баланс банкомату"""
        query = self.cursor.execute("SELECT * FROM money_bills").fetchall()
        atm_balance = sum([x[0] * x[1] for x in query])
        return atm_balance

    def all_nominal(self) -> list:
        """Повертає список номінальних банкнот"""
        query = self.cursor.execute(
            "SELECT * FROM money_bills ORDER BY bill DESC").fetchall()
        return [i[0] for i in query for _ in range(i[1])]

    def dict_nominal(self) -> dict:
        """Словник доступних в банкоматі банкнот"""
        query = self.cursor.execute(
            "SELECT * FROM money_bills ORDER BY bill DESC").fetchall()
        return {i[0]: i[1] for i in query}

    def min_banknotes(self) -> int:
        """Мінімальна банкнота, яку використовує банкомат"""
        return self.cursor.execute(
            "SELECT MIN(bill) FROM money_bills").fetchone()[0]

    def get_all_statements(self) -> list:
        """Повертає всю виписку всіх транзакцій"""
        query = self.cursor.execute("""SELECT * FROM statement ORDER BY id DESC """).fetchall()
        return [i for i in query]

    def get_user_statement(self) -> list:
        """Виписка транзакцій клієнта"""
        return self.cursor.execute(
            """SELECT orders FROM statement WHERE username = ?
                ORDER BY id DESC""", (self.login,)).fetchall()

    def change_bills(self) -> str:
        """Змінює кількість банкнот в банкоматі"""
        add_money = self.dict_nominal()
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
                with self.conn:
                    self.cursor.execute(
                        "UPDATE money_bills SET count = ? WHERE bill = ?",
                        (result, choose)
                    )
                self.conn.commit()
                self.write_statement(
                    desc="Change money",
                    amount={choose: amount},
                    balance={choose: result}
                )
                return f"Banknote 💵${choose} has been changed to " \
                       f"{amount} pcs.Now 💵${choose} total: {result} pcs."
        else:
            return "Not found banknote"

    def make_deposit(self) -> tuple:
        """Поповнює баланс"""
        min_bill = self.min_banknotes()
        current_balance = self.get_user_balance()
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

            self.change_user_balance(new_balance)
            self.write_statement(
                desc="Deposit", amount=deposit, balance=new_balance)

            print(Fore.LIGHTGREEN_EX +
                  f"{self.login.capitalize()}, "
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

    def show_plot(self):
        """Показує графік поповнень рахунку"""

        statement = self.get_user_statement()
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

    def withdraw_balance(self, amount_funds) -> list:
        """Оновлює кількість номіналів купюр"""

        # список всіх купюр із банкомата
        kit = self.all_nominal()
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
            sums = sums | new_sums  # додаємо (об'єднуємо) значення
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
        db_upload = self.dict_nominal()

        # формуємо словник з кількістю номіналів купюр
        db_out = {i: withdraw_banknotes.count(i) for i in withdraw_banknotes}

        # віднімаємо видані купюри
        for key, value in db_out.items():
            db_upload[key] -= value

        # Оновлюємо БД з новим залишком
        for bill, count in db_upload.items():
            with self.conn:
                self.cursor.execute(
                    "UPDATE money_bills SET count = ? WHERE bill= ?", (count, bill)
                )
            self.conn.commit()
        return withdraw_banknotes

    def make_withdraw(self) -> tuple:
        """Знімає кошти, зменшує баланс"""

        min_bill = self.min_banknotes()  # мінімальний номінал з АТМ
        amount = abs(int(input(Fore.LIGHTMAGENTA_EX +
                               "What amount to withdraw?: $").strip()))
        current_balance = self.get_user_balance()
        new_balance = current_balance - amount
        atm_balance = self.get_atm_balance()

        if atm_balance - amount >= 0 and new_balance >= 0:
            if amount % min_bill == 0:
                try:
                    print("Your banknotes:", self.withdraw_balance(amount))
                except AtmException as ex:
                    print(ex)
                    self.make_withdraw()
                else:
                    self.change_user_balance(new_balance)
                    self.write_statement(
                        desc="Withdraw",
                        amount=-amount,
                        balance=new_balance
                    )
                    print(Fore.LIGHTGREEN_EX +
                          f"{self.login.capitalize()}, "
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
                             f"${self.get_user_balance()}{Style.RESET_ALL}"
                             f"{Fore.RED}, ATM balance: {Back.LIGHTWHITE_EX}"
                             f"${atm_balance}{Style.RESET_ALL}"
                  )

    def validate_same_password(self, passwd: str) -> str:
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
                if self.validate_diff_passwd(new_password):
                    break
            return self.validate_same_password(new_password)

    @staticmethod
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

    def sign_up(self):
        """Реєстрація нового клієнта"""
        print(Fore.LIGHTRED_EX + "Registration".center(100, '~'))
        with self.conn:
            users = self.cursor.execute("SELECT username FROM users").fetchall()

        client = input("Input username: ").strip()
        if client in [name[0] for name in users]:
            print('Name is already registered, try again with unique name')
            return self.sign_up()

        while True:
            passwd = input(Fore.LIGHTMAGENTA_EX + "Enter password: ").strip()
            if self.validate_diff_passwd(passwd):
                break

        password = self.validate_same_password(passwd)
        # Шанс 10% на баланс в $100
        bonus = 100 if random.random() < 0.1 else 0
        with self.conn:
            self.cursor.execute(
                """INSERT INTO users (username, password, balance, staff)
                    VALUES (?,?,?,?)""", (client, password, bonus, "client")
            )
        self.conn.commit()
        print(Fore.GREEN +
              "Registered done. Wellcome to ATM!".center(100, '~'))
        return Menu(client, password).client_menu()


class Menu:
    """Меню банкомата в залежності від прав користувача"""

    def __init__(self, login, passwd):
        self.client = Atm(login, passwd)

    # Меню клієнта
    def client_menu(self):
        choice = input("Select:\n"
                       "1️⃣ - Balance\n"
                       "2️⃣ - Deposit\n"
                       "3️⃣ - Withdraw\n"
                       "4️⃣ - Statement\n"
                       "5️⃣ - Deposit chart\n"
                       "6️⃣ - Log Out\n"
                       "Make your choice: ")

        if choice == "1":
            balance = self.client.get_user_balance()
            print(Fore.YELLOW + f"Your balance is "
                                f"{Fore.BLACK}{Back.YELLOW}${balance}"
                                f"{Style.RESET_ALL}\n")
        elif choice == "2":
            self.client.make_deposit()

        elif choice == "3":
            self.client.make_withdraw()

        elif choice == "4":
            statement = self.client.get_user_statement()
            [print(i[0], end="\n") for i in statement]

        elif choice == "5":
            self.client.show_plot()

        elif choice == "6":
            main()
        else:
            print("Wrong input, please try again...")

        return self.client_menu()

    # Меню інкасатора
    def collector_menu(self):
        choice = input("Select:\n"
                       "1 - Balance\n"
                       "2 - Change Banknotes\n"
                       "3 - Statement\n"
                       "4 - Log Out\n"
                       "Make your choice: ")

        if choice == "1":
            print(Fore.BLACK + Back.LIGHTYELLOW_EX +
                  f"ATM balance: ${self.client.get_atm_balance()}{Style.RESET_ALL}\n"
                  f"Content availability:")
            for bill, count in self.client.dict_nominal().items():
                print("💰", bill, "⇢", count, "pcs")
        elif choice == "2":
            print(Fore.BLACK +
                  Back.LIGHTYELLOW_EX + self.client.change_bills())
        elif choice == "3":
            statement = self.client.get_all_statements()
            if statement:
                [print(i, end="\n") for i in sorted(statement, key=lambda x: x[1])]
            else:
                print("Not found.There is no transaction at the ATM!")

        elif choice == "4":
            main()
        else:
            print("Wrong input, please try again...")

        return self.collector_menu()


def main():
    # Головне МЕНЮ
    choice = input("MENU:\n"
                   "1 - Sign In\n"
                   "2 - Sign Up\n"
                   "3 - Exit\n"
                   "Make your choice: ").strip()

    if choice == "1":
        login = input('Please input your login: ').strip()
        password = input('Input password: ').strip()
        start_use = Atm(login, password)

        if start_use.auth_validate() and start_use.access_level() == "client":
            print("Welcome to ATM")
            menu = Menu(login, password)
            menu.client_menu()

        elif start_use.auth_validate() and start_use.access_level() == "collector":
            print("Settings to ATM")
            menu = Menu(login, password)
            menu.collector_menu()
        else:
            print("Access denied")
            main()

    elif choice == "2":
        Atm().sign_up()

    elif choice == "3":
        exit()
    else:
        print("Wrong input, try again...")
        main()


if __name__ == '__main__':
    main()
