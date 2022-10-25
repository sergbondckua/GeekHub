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


def my_range(*args):
    """Custom range func"""
    if not args:
        raise TypeError('Range expected at least 1 argument, got 0')

    if len(args) == 1:
        num = 0
        while num != args[0]:
            yield num
            if args[0] > 0:
                num += 1
            else:
                num -= 1
    elif len(args) == 2:
        num = args[0]
        while num != args[1]:
            yield num
            if args[0] < args[1]:
                num += 1
            else:
                num -= 1
    elif len(args) == 3:
        if (args[0] < args[1] and args[2] > 0) or (args[0] > args[1] and args[2] < 0):
            num = args[0]
            if num < args[1]:
                while num < args[1]:
                    yield num
                    num += args[2]
            else:
                while num > args[1]:
                    yield num
                    num += args[2]
        else:
            raise Exception("Fail range")
    else:
        raise Exception("Overdose args")
    return None


if __name__ == '__main__':
    print(list(my_range(1, 10, 2)))
