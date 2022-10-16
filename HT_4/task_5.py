"""
Ну і традиційно - калькулятор
Повинна бути 1 функцiя, яка приймає 3 аргументи - один з яких операцiя,
яку зробити! Аргументи брати від юзера (можна по одному - окремо 2, окремо +,
окремо 2; можна всі разом - типу 2 + 2).
Операції що мають бути присутні: +, -, *, /, %, //, **.
Не забудьте протестувати з різними значеннями на предмет помилок!
"""


def calculator(expression):
    """Just Calc"""
    operators = ('+', '-', '*', '/', '%', '//', '**')
    if not any(mark in expression for mark in operators):
        print(f'У виразі має бути присутній один із {operators} операторів')
        # raise ValueError(f'У виразі має бути присутній один із {operators} операторів')

    for mark in operators:
        if mark in expression:
            try:
                left_val, right_val = map(int, expression.split(mark))
                print(left_val, mark, right_val, '=')
                process = {
                    '+': lambda x, y: x + y,
                    '-': lambda x, y: x - y,
                    '/': lambda x, y: x / y,
                    '//': lambda x, y: x // y,
                    '*': lambda x, y: x * y,
                    '**': lambda x, y: x ** y,
                    '%': lambda x, y: x % y,
                }
                return process[mark](left_val, right_val)
            except ZeroDivisionError:
                print('На "0" ділити не можна!')

                # raise ZeroDivisionError('На "0" ділити не можна!')
            except (ValueError, TypeError):
                print('Неправильно вказаний вираз, має бути 2 цілих'
                      ' числа та 1 оператор')

                # raise ValueError('Неправильно вказаний вираз,'
                #                  'має бути 2 цілих числа та 1 оператор')


if __name__ == '__main__':
    print(calculator('2+2'))
