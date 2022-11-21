"""
Напишіть програму, де клас «геометричні фігури» (Figure) містить властивість
color з початковим значенням white і метод для зміни кольору фігури,
а його підкласи «овал» (Oval) і «квадрат» (Square) містять методи _init_
для завдання початкових розмірів об'єктів при їх створенні.
"""


class Figure:
    """Базовий клас"""
    color = "white"

    def change_color(self, new_color: str):
        self.color = new_color


class Oval(Figure):
    """Субклас, овал"""

    def __init__(self, size_long: int, size_width: int):
        self.size_width = size_width
        self.size_long = size_long

    def print_info(self):
        print(f"Color: {self.color}\nSize: {self.size_long, self.size_width}")


class Square(Figure):
    """Квадрат"""

    def __init__(self, size_side: int):
        self.size_side = size_side

    def print_info(self):
        print(f"Color: {self.color}\nSize: {self.size_side}")


if __name__ == '__main__':
    # Oval
    Oval(12, 4).print_info()

    # Square
    fig_1 = Square(5)
    fig_1.change_color("red")
    fig_1.print_info()
