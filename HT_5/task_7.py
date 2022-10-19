"""
 Написати функцію, яка приймає на вхід список (через кому), підраховує
 кількість входження кожного елемента в послідовність і виводить результат.
 Елементами списку можуть бути дані будь-яких типів.
    Наприклад:
    1, 1, 'foo', [1, 2], True, 'foo', 1, [1, 2] ----> "1 -> 3, foo -> 2, [1, 2] -> 2, True -> 1"
"""
from collections import Counter


# Solution #1 without import module
def count_element(lst):
    """ Count element in the sequence"""

    lst_str = list(map(str, lst))
    solution = [(item, lst_str.count(item),) for item in set(lst_str)]
    print('#1 Solution:', ', '.join(f"{item[0]} -> {item[1]}" for item in solution))

    return solution


# Solution #2 with import module
def count_element2(lst):
    """ Count element in the sequence"""

    lst_str = list(map(str, lst))
    solution = dict(Counter(lst_str))
    print('#2 Solution:', ', '.join(f"{val} -> {count}" for val, count in solution.items()))

    return solution


if __name__ == '__main__':
    count_element([1, 1, 'foo', [1, 2], True, 'foo', 1, [1, 2]])

    # with import module
    count_element2([1, 1, 'foo', [1, 2], True, 'foo', 1, [1, 2]])
