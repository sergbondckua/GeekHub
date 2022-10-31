"""
Написати функцію <square>, яка прийматиме один аргумент - сторону квадрата,
і вертатиме 3 значення у вигляді кортежа: периметр квадрата,
площа квадрата та його діагональ.
"""
import math


def square(side):
    """Get area, perimeter, diagonal"""

    area = side ** 2
    perimeter = 4 * side
    diagonal = round(side * math.sqrt(2), 2)
    return perimeter, area, diagonal


if __name__ == '__main__':
    square(5)
