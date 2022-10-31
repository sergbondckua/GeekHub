"""
Напишіть функцію,яка приймає рядок з декількох слів і повертає довжину
найкоротшого слова. Реалізуйте обчислення за допомогою генератора в один рядок.
"""


def short_word(str_text: str) -> int:
    """The shortest word in a phrase"""
    return min([len(word) for word in str_text.split()])


if __name__ == '__main__':
    print(short_word(input("Enter your phrase:\n")))
