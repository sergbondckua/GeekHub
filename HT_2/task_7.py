"""
Напишіть сценарій, щоб об’єднати всі елементи списку в рядок і надрукувати його.
Список має включати як рядки, так і цілі числа та мати жорсткий код.
"""

my_elements_list = ['My', 'some', 100, 'text', 'and', 11.00, 'int', 6, 'or', 'float', -3]

print(' '.join(map(str, my_elements_list)))

