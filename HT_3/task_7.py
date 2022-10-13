"""
Напишіть сценарій, який приймає <число>(int) від користувача
та генерує словник у діапазоні <число>,
де ключ — <число>, а значення — <число>*<число>
напр. 3 --> {0: 0, 1: 1, 2: 4, 3: 9}
"""

*number, = range(int(input('Enter a number: ')) + 1)

# Using cycles
print({i: i ** 2 for i in number})

# Not using cycles
print(dict(zip(number, map(lambda x: x ** 2, number))))
