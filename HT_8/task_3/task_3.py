"""Банкомат"""

import csv
import json
import random
from datetime import datetime


def validate_user_access(func):
    """Декоратор на валідність логіна та пароля"""

    def wrapper(login: str, passwd: str, *args, **kwargs):
        # Відкриває файл с даними доступу
        with open("db/users.csv", "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['username'] == login and row['password'] == passwd:
                    return func(login, passwd, *args, **kwargs)
            raise Exception("Access denied!")

    return wrapper


def write_statement(client: str, *args, **kwargs):
    """Записує в файл транзакції клієнта"""
    data = {
        "id": random.randint(0, 99999999),
        "time": datetime.now().timestamp().__int__(),
        "description": kwargs["desc"],
        "amount": kwargs["amount"],
        "balance": kwargs["balance"]
    }
    try:
        with open("asset/" + client + "_transactions.json", "r+", encoding="utf-8") as f:
            file_data = json.load(f)
            file_data.append(data)

        with open("asset/" + client + "_transactions.json", "w", encoding="utf-8") as f:
            json.dump(file_data, f, indent=4)
    except FileNotFoundError:
        with open("asset/" + client + "_transactions.json", "w", encoding="utf-8") as f:
            json.dump([data], f, indent=4)


@validate_user_access
def sign_in(login, passwd):
    """Повертає словник з даними доступа клієнта"""
    print(f"\nHello {login.capitalize()}, access successfully\n")
    return dict(login=login, password=passwd)


def get_balance(client: str):
    """Отримує баланс клієнта"""
    try:
        with open("asset/" + client + "_balance.txt", "r") as f:
            balance = f.read()
            return balance
    except FileNotFoundError as e:
        with open("asset/" + client + "_balance.txt", "w") as f:
            balance = "0"
            f.write(balance)
    return 0


def make_deposit(client: str) -> tuple:
    """Поповнює баланс"""
    current_balance = get_balance(client)
    deposit = round(abs(float(input("Enter your deposit: $"))), 2)
    new_balance = round(float(current_balance) + deposit, 2)
    with open("asset/" + client + "_balance.txt", "w", encoding="utf-8") as f:
        f.write(str(new_balance))
        write_statement(client, desc="Deposit", amount=deposit, balance=new_balance)
    return deposit, new_balance


def make_withdraw(client: str):
    """Знімає кошти, зменшує баланс"""
    amount = round(abs(float(input("What amount to withdraw?: $"))), 2)
    current_balance = get_balance(client)
    new_balance = round(float(current_balance) - amount, 2)
    if new_balance > 0:
        with open("asset/" + client + "_balance.txt", "w", encoding="utf-8") as f:
            f.write(str(new_balance))
            write_statement(client, desc="Withdraw", amount=amount, balance=new_balance)
        return amount, new_balance
    else:
        print(f"It is not possible to withdraw ${amount}, "
              f"your balance: ${get_balance(client)}\n", '####' * 10)
    return False


def start():
    print("Authorization required: Sign in please")
    username = input("Enter a username: ")
    password = input("Enter your password: ")
    client = sign_in('tom', 'q12345')
    stop = True
    while stop:
        choose = input(
            "CHOOSE AN ITEM:\n[1] - Balance -\n[2] - Deposit -\n"
            "[3] - Withdraw -\n[4] - EXIT -\n"
        )
        # Select 1
        if choose == "1":
            print(f"[BALANCE]\n", "####" * 10)
            balance = get_balance(client.get('login'))
            print(f"{client['login'].capitalize()}, "
                  f"your balance is ${balance}\n", "####" * 10)

        # Select 2
        elif choose == "2":
            print("[DEPOSIT]\n", "####" * 10)
            deposit = make_deposit(client.get('login'))
            print(f"{client['login'].capitalize()}, now +${deposit[0]} and "
                  f"your new balance is ${deposit[1]}\n", "####" * 10)

        # Select 3
        elif choose == "3":
            print("[WITHDRAW]\n", "####" * 10)
            withdraw = make_withdraw(client.get('login'))
            if withdraw:
                print(f"{client['login'].capitalize()}, now -${withdraw[0]} and "
                      f"your new balance is ${withdraw[1]}\n", "####" * 20)

        # Select 4
        elif choose == "4":
            print("[EXIT]\n", "####" * 10)
            print(f"Bye-bye, {client['login'].capitalize()}!\n", "####" * 10)
            stop = False


if __name__ == '__main__':
    start()
