"""
Створити клас Calc, який буде мати атрибут last_result та 4 методи.
Методи повинні виконувати математичні операції з 2-ма числами,
а саме додавання, віднімання, множення, ділення.
- Якщо під час створення екземпляру класу звернутися до атрибута last_result
він повинен повернути пусте значення.
- Якщо використати один з методів - last_result повинен повернути результат
виконання ПОПЕРЕДНЬОГО методу.
    Example:
    last_result --> None
    1 + 1
    last_result --> None
    2 * 3
    last_result --> 2
    3 * 4
    last_result --> 6
    ...
"""


class Calc:
    """Performs math operations with 2 numbers
    Methods:
        One more other documentation
    """
    last_result = None

    def addition(self, num, num2) -> int | float:
        print(self.last_result)
        self.last_result = num + num2
        return self.last_result

    def subtraction(self, num, num2) -> int | float:
        print(self.last_result)
        self.last_result = num - num2
        return self.last_result

    def multiplication(self, num, num2) -> int | float:
        print(self.last_result)
        self.last_result = num * num2
        return self.last_result

    def division(self, num, num2) -> float:
        print(self.last_result)
        try:
            self.last_result = num / num2
        except ZeroDivisionError as ex:
            self.last_result = ex
        return self.last_result


if __name__ == '__main__':
    result = Calc()

    result.addition(1, 1)
    result.multiplication(2, 3)
    result.division(3, 0)
    result.subtraction(3, 1)

    print(Calc.__doc__)
