"""
Написати функцію <prime_list>, яка прийматиме 2 аргументи
- початок і кінець діапазона,
і вертатиме список простих чисел всередині цього діапазона.
Не забудьте про перевірку на валідність введених даних та
у випадку невідповідності - виведіть повідомлення.
"""


def prime_list(start, end):
    """ Number is prime list"""
    lst = []

    for number in range(start, end + 1):
        if number > 1:
            for i in range(2, number):
                if number % i == 0:
                    break
            else:
                lst.append(number)
        else:
            print('Початкове значення діапазону має бути більше "1"')
            return None

    return lst


if __name__ == '__main__':
    print(prime_list(5, 17))
