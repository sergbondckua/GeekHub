"""
Реалізуйте генератор, який приймає на вхід будь-яку ітерабельну послідовність
(рядок, список, кортеж) і повертає генератор, який буде повертати значення з
цієї послідовності, при цьому, якщо було повернено останній елемент із
послідовності - ітерація починається знову.
"""


def generator(iterable):
    """ Infinite iteration of elements"""
    while True:
        for element in iterable:
            yield element


if __name__ == '__main__':
    for elem in generator(['infinity', 'iterables', '1', '2', '3']):
        print(elem)
