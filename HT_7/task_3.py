"""
Всі ви знаєте таку функцію як <range>. Напишіть свою реалізацію цієї функції.
Тобто щоб її можна було використати у вигляді:
    for i in my_range(1, 10, 2):
        print(i)
    1
    3
    5
    7
    9
   P.S. Повинен вертатись генератор.
   P.P.S. Для повного розуміння цієї функції - можна почитати документацію по
   ній: https://docs.python.org/3/library/stdtypes.html#range
   P.P.P.S Не забудьте обробляти невалідні ситуації (типу range(1, -10, 5)
   тощо). Подивіться як веде себе стандартний range в таких випадках.
"""


def my_range(first, second=None, third=None):
    """ Custom range func """
    if second is None:
        if not isinstance(first, int):
            raise TypeError("Parameter is not an integer")
        start = 0
        stop = first
        step = 1
    elif third is None:
        if not isinstance(second, int):
            raise TypeError("Parameter is not an integer")
        start = first
        stop = second
        step = 1
    else:
        if not isinstance(third, int):
            raise TypeError("Parameter is not an integer")
        if third == 0:
            raise ValueError("Parameter cannot be zero")
        start = first
        stop = second
        step = third
        if (start > stop and step > 0) or (start < stop and step < 0):
            raise Exception("Fail range: parameters is incorrect")

    num = start
    if step > 0:
        while num < stop:
            yield num
            num += step
    elif step < 0:
        while num > stop:
            yield num
            num += step


if __name__ == '__main__':
    print(list(my_range(1, 10, 2)))
