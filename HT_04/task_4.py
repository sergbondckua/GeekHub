"""
Наприклад маємо рядок
--> "f98neroi4nr0c3n30irn03ien3c0rfe
kdno400we(nw,kowe%00koi!jn35pijnp4 6ij7k5j78p3kj546p4 ->
просто потицяв по клавi =)
Створіть ф-цiю, яка буде отримувати довільні рядки
на зразок цього та яка обробляє наступні випадки:
-  якщо довжина рядка в діапазоні 30-50 (включно)
-> прiнтує довжину рядка, кiлькiсть букв та цифр
-  якщо довжина менше 30
-> прiнтує суму всіх чисел та окремо рядок без цифр та
знаків лише з буквами (без пробілів)
-  якщо довжина більше 50
-> Друкує тільки голосні
"""


def chaotic_taps(random_str: str):
    """Output depending on the length"""

    len_str = len(random_str)
    digit_only = [int(i) for i in random_str if i.isdigit()]
    alpha_only = [a for a in random_str if a.isalpha()]
    vowels = [i for i in random_str if i.lower() in ('a', 'e', 'i', 'o', 'u')]

    if 30 <= len_str <= 50:

        print(f"Lenght: {len_str}, "
              f"Lenght alpha: {len(alpha_only)}, "
              f"Lenght digit {len(digit_only)}")

    elif len_str < 30:
        print(f"Sum: {sum(digit_only)}, "
              f"Only alpha: {''.join(alpha_only)}")

    else:
        print(f"Vowels: {''.join(vowels)}")


if __name__ == '__main__':
    chaotic_taps(input("Enter the chaotic taps:\n"))
