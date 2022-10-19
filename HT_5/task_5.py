"""
Написати функцію <fibonacci>, яка приймає один аргумент і виводить
всі числа Фібоначчі, що не перевищують його.
"""


def fibonacci(num):
    """ Return fibonacci"""

    lst = [1, 1]

    for i in range(2, num):
        if lst[-1] + lst[-2] <= num:
            lst.append(lst[-1] + lst[-2])
    print(', '.join(map(str, lst)))

    return lst


if __name__ == '__main__':
    fibonacci(21)
