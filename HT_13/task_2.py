"""
Створити клас Matrix, який буде мати наступний функціонал:
__init__ - вводиться кількість стовпців і кількість рядків
fill() - заповнить створений масив числами - по порядку.
print_out() - виведе створений масив
(якщо він ще не заповнений даними - вивести нулі
transpose() - перевертає створений масив.
Тобто, якщо взяти попередню таблицю, результат буде
"""


class Matrix:
    """Матриця з функціоналом"""

    def __init__(self, row: int, column: int):
        self.column = column
        self.row = row
        self.matrix = [[0] * column for _ in range(row)]

    def fill(self) -> None:
        """Заповнює створений масив числами - по порядку"""
        self.matrix = [[*range(1 + self.column * i, 1 + self.column * (i + 1))]
                       for i in range(self.row)]

    def print_out(self) -> list:
        """Повертає створений масив"""
        return self.matrix

    def transpose(self) -> list:
        """Транспонує масив"""
        return [[self.matrix[j][i] for j in range(len(self.matrix))]
                for i in range(len(self.matrix[0]))]


if __name__ == '__main__':
    some_matrix = Matrix(row=3, column=2)  # Створюємо екземпляр класу
    some_matrix.fill()  # Заповнюємо матрицю
    print(some_matrix.print_out())  # Виводимо створену матрицю
    print(some_matrix.transpose())  # Транспонуємо
