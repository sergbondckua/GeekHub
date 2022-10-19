"""
 Написати функцію, яка приймає на вхід список (через кому),
 підраховує кількість однакових елементів у ньому і виводить результат.
 Елементами списку можуть бути дані будь-яких типів.
    Наприклад:
    1, 1, 'foo', [1, 2], True, 'foo', 1, [1, 2] ----> "1 -> 3, foo -> 2, [1, 2] -> 2, True -> 1"
"""
from collections import Counter


def count_element(lst):
    """ Count same elements"""

    lst_str = list(map(str, lst))

    solution = [(item, lst_str.count(item),) for item in set(lst_str) if lst_str.count(item) > 1]
    print(', '.join(f"{item[0]} -> {item[1]}" for item in solution))

    solution2 = dict(Counter(lst_str))
    print(', '.join(f"{val} -> {count}" for val, count in solution2.items()))

    return solution2  # solution


if __name__ == '__main__':
    count_element([1, 1, 'foo', [1, 2], True, 'foo', 1, [1, 2]])
