"""
Створіть клас в якому буде атрибут,
який буде рахувати кількість створених екземплярів класів.
"""


class CountsClassInstances:
    """Рахує кількість створених екземплярів класу"""
    count = 0

    def __init__(self):
        CountsClassInstances.count += 1

    def __str__(self):
        return str(self.count)


if __name__ == '__main__':
    first = CountsClassInstances()
    print(first)

    second = CountsClassInstances()
    print(second)

    third = CountsClassInstances()
    print(third)
