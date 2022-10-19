"""
Написати функцию <is_prime>, яка прийматиме 1 аргумент - число від 0 до 1000,
и яка вертатиме True, якщо це число просте і False - якщо ні.
"""


def is_prime(number):
    """ Checking number is prime"""
    if number in range(1001):
        if number % 2 == 0:
            return number == 2

        i = 3
        while i ** 2 <= number and number % i != 0:
            i += 2
        return i ** 2 > number

    print('Введене число має бути від 0 до 1000')
    return None


if __name__ == '__main__':
    print(is_prime(7))
