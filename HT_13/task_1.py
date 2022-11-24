"""
Створіть клас Car, який буде мати властивість year (рік випуску).
Додайте всі необхідні методи до класу, щоб можна було виконувати порівняння
car1 > car2, яке буде показувати, що car1 старша за car2.
Також, операція car1 - car2 повинна повернути різницю між роками випуску.
"""
from functools import total_ordering


@total_ordering
class Car:
    """Порівняння властивостей"""

    def __init__(self, release_year: int):
        self.release_year = release_year

    def __eq__(self, other):
        return self.release_year == other.release_year and \
               other.release_year == self.release_year

    def __lt__(self, other):
        return self.release_year > other.release_year

    def __sub__(self, other):
        return self.release_year - other.release_year

    def __str__(self):
        return str(self.release_year)


if __name__ == '__main__':
    car1 = Car(2008)
    car2 = Car(2020)

    print(f"Car {car1} > Car {car2}:", car1 > car2)
    print(f"Car {car2} - Car {car1} = ", car2 - car1)
