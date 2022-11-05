import sqlite3
import json
import random
from datetime import datetime
from colorama import init, Fore, Back, Style

init(autoreset=True)  # Автоматичне додавання Style.RESET_ALL в кінець print

conn = sqlite3.connect('atm.db')


# cursor = conn.cursor()


def auth_validate(login: str, passwd: str):
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
                    for attempt in range(2):
                        if user[1] == input(
                                f"Incorrect password, try again: "):
                            return True
                        else:
                            print(f"Try again, last attempt!")
                    raise Exception("Access denied!")

        # Якщо клієнта немає в БД, пропонуємо реєстрацію
        print(Fore.LIGHTGREEN_EX + "Not found username, need registration")
        if input("You want sign_up? - yes/no: ").strip() in ["yes", "y"]:
            return sign_up(login)
        raise Exception("Access denied, Bye!")

    except sqlite3.OperationalError as ex:
        print("[INFO] Error while working with SQLite3,", ex)
    except Exception as ex:
        print(ex)

    return False


def sign_up(client):
    """Реєстрація нового клієнта"""
    print(Fore.LIGHTRED_EX + "Registration".center(100, '~'))
    with conn:
        cursor = conn.cursor()
        users = cursor.execute("SELECT username FROM users").fetchall()
        if client in users:
            print('Name is already registered, try again with unique name')
            return main()

        pre_passwd = input(f"Enter your new password for {client}: ")
        repeat_passwd = input("Repeat your password: ")
        passwd = pre_passwd if repeat_passwd == pre_passwd else False
        if not passwd:
            print("Passwords don't match")
            return sign_up(client)

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


def get_balance(client: str):
    """Отримує баланс клієнта"""
    with conn:
        cursor = conn.cursor()
        balance = cursor.execute(
            "SELECT balance FROM users WHERE username = :client",
            {"client": client}).fetchone()
        return balance[0]


def make_deposit(client: str) -> tuple:
    """Поповнює баланс"""
    with conn:
        cursor = conn.cursor()
        min_bill = cursor.execute(
            "SELECT MIN(bill) FROM money_bills").fetchone()[0]

        current_balance = get_balance(client)
        deposit = abs(int(input("Enter your deposit: $")))
        new_balance = current_balance
        rest = deposit % min_bill

        if deposit > min_bill:  # Якщо введена сума більша за мінімальну купюру
            if rest != 0:  # Якщо не кратна мінімальній купюрі
                new_balance += deposit - rest
                deposit -= rest
                print(Fore.RED + f"Bills are not supported, refund: ${rest}")

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
                  f"${new_balance}{Style.RESET_ALL}\n"
                  )
        else:
            print(Back.LIGHTRED_EX +
                  f"Bills are not supported! Refund money: ${deposit}"
                  f"{Style.RESET_ALL}\n")
        return deposit, new_balance


def make_withdraw(client: str):
    """Знімає кошти, зменшує баланс"""
    amount = abs(int(input("What amount to withdraw?: $")))
    current_balance = get_balance(client)
    new_balance = current_balance - amount
    with conn:
        cursor = conn.cursor()
        query = cursor.execute("SELECT * FROM money_bills").fetchall()
        atm_balance = sum([x[0] * x[1] for x in query])

    if new_balance > 0 and atm_balance - amount > 0:
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                f"""UPDATE users SET balance = ?
                    WHERE username = ?""", (new_balance, client))
            conn.commit()
            write_statement(client, desc="Withdraw", amount=-amount, balance=new_balance)
            return amount, new_balance
    else:
        print(Fore.RED + f"It is not possible to withdraw "
                         f"{Fore.BLACK}{Back.RED}${amount}{Style.RESET_ALL}"
                         f"{Fore.RED}, your balance: {Back.LIGHTWHITE_EX}"
                         f"${get_balance(client)}{Style.RESET_ALL}"
                         f"{Fore.RED}, ATM balance: {Back.LIGHTWHITE_EX}"
                         f"${atm_balance}{Style.RESET_ALL}"
              )
    return None


def add_bills(login: str):
    """Add money in ATM"""
    with conn:
        cursor = conn.cursor()
        money = cursor.execute("SELECT * FROM money_bills").fetchall()
        add_money = list(map(list, money))

        for i in range(len(add_money)):
            add = int(input(f"How much to add to this bill? {money[i][0]}: "))
            add_money[i][1] += abs(add)
            cursor.execute(
                "UPDATE money_bills SET count = ? WHERE bill = ?",
                (add_money[i][1], add_money[i][0])
            )
        conn.commit()


def revision_bills(login: str):
    """Check money in ATM"""
    print("Content availability:")
    with conn:
        cursor = conn.cursor()
        money = cursor.execute("SELECT * FROM money_bills").fetchall()
        for item in money:
            print("💰", item[0], "⇢", item[1], "pcs")


def staff_menu(login):
    choice = input("Select:\n"
                   "1️⃣ - Add money\n"
                   "2️⃣ - Revision money\n"
                   "3️⃣ - EXIT\n"
                   )
    choices = {
        "1": add_bills,
        "2": revision_bills,
        "3": 3,
    }
    choices[choice](login)


def main():
    print(Fore.CYAN + "Authorization required: Sign in please!")
    username = input("Enter a username: ")
    password = input("Enter your password: ")
    run = True

    if auth_validate(username, password):
        print(
            Fore.CYAN + f"\nHello {username.capitalize()}, "
                        f"access successfully\n" + Style.RESET_ALL
        )
        while run:
            choose = input(Fore.LIGHTBLACK_EX +
                           f"CHOOSE AN ITEM:{Style.RESET_ALL}\n"
                           f"{Fore.LIGHTYELLOW_EX}[1] - Balance{Style.RESET_ALL}\n"
                           f"{Fore.GREEN}[2] - Deposit{Style.RESET_ALL}\n"
                           f"{Fore.MAGENTA}[3] - Withdraw{Style.RESET_ALL}"
                           f"{Fore.RESET}\n[4] - EXIT\n" + Style.RESET_ALL
                           )
            # Select 1
            if choose == "1":
                print(f"[BALANCE]".center(30, "#"))
                balance = get_balance(username)
                print(Fore.YELLOW + f"{username.capitalize()}, "
                                    f"your balance is "
                                    f"{Fore.BLACK}{Back.YELLOW}${balance}"
                                    f"{Style.RESET_ALL}\n"
                      )

            # Select 2
            elif choose == "2":
                print("[DEPOSIT]".center(30, "#"))
                deposit = make_deposit(username)

            # Select 3
            elif choose == "3":
                print("[WITHDRAW]".center(30, "#"))
                withdraw = make_withdraw(username)
                if withdraw:
                    print(Fore.LIGHTGREEN_EX +
                          f"{username.capitalize()}, "
                          f"now {Back.LIGHTBLACK_EX}-${withdraw[0]}"
                          f"{Style.RESET_ALL + Fore.LIGHTGREEN_EX} and "
                          f"your new balance is {Back.LIGHTBLACK_EX}"
                          f"${withdraw[1]}{Style.RESET_ALL}\n"
                          )

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