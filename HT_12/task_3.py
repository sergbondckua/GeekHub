"""
Створіть клас в якому буде атрибут,
який буде рахувати кількість створених екземплярів класів.
"""


class CountsClassInstances:
    """Рахує кількість створених екземплярів класу"""
    count = 0

    def __init__(self):
        self.__class__.count += 1


if __name__ == '__main__':

    first = CountsClassInstances()
    second = CountsClassInstances()
    third = CountsClassInstances()

    print(CountsClassInstances().count)
