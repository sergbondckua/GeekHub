"""
Написати функцію, яка буде реалізувати логіку циклічного зсуву елементів
в списку. Тобто функція приймає два аргументи: список і величину зсуву
(якщо ця величина додатна - пересуваємо з кінця на початок,
якщо від'ємна - навпаки - пересуваємо елементи з початку списку в його кінець).
   Наприклад:
   fnc([1, 2, 3, 4, 5], shift=1) --> [5, 1, 2, 3, 4]
   fnc([1, 2, 3, 4, 5], shift=-2) --> [3, 4, 5, 1, 2]
"""


def landslide(lst, shift):
    """ Shifts elements"""

    slide = []
    if shift > 0:
        for _ in range(shift):
            slide.append(lst.pop(-1))

        return slide + lst
    else:
        for _ in range(abs(shift)):
            slide.append(lst.pop(0))

        return lst + slide


if __name__ == '__main__':
    print(landslide([1, 2, 3, 4, 5], shift=-2))
