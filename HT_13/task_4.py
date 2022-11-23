"""
Створіть клас, який буде повністю копіювати поведінку list,
за виключенням того, що індекси в ньому мають починатися з 1, а індекс 0
має викидати помилку (такого ж типу,
яку кидає list якщо звернутися до неіснуючого індексу)
"""


class CustomList(list):
    """List without index 0"""

    def __getitem__(self, index: int):
        if index == 0:
            raise IndexError("list index out of range")
        index -= 1
        return super().__getitem__(index)


if __name__ == '__main__':
    ls = CustomList([1, 3, 4, 5])
    print(ls[-1])
    print(ls[0])
