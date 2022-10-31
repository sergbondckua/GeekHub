"""
Створіть 3 рiзних функцiї (на ваш вибiр).
Кожна з цих функцiй повинна повертати якийсь результат (напр. інпут від юзера,
результат математичної операції тощо). Також створiть четверту ф-цiю,
яка всередині викликає 3 попередні,
обробляє їх результат та також повертає результат своєї роботи.
Таким чином ми будемо викликати одну (четверту) функцiю,
а вона в своєму тiлi - ще 3.
"""

from datetime import datetime


# First
def is_leap(year):
    """ Determines the leap year"""
    leap_year = False
    if year % 4 == 0:
        leap_year = True
        if year % 100 == 0 and year % 400 != 0:
            leap_year = False
    return leap_year


# Second
def get_age(year):
    """ Returns the age"""
    return datetime.now().year - year


# Third
def go_to_school(year):
    """A year to go to school"""
    return year + 7


# Fourth
def about_you():
    """ Return a short description about the user"""
    year = int(input('Введіть свій рік народження:\n'))
    this_year = 'високосний' if is_leap(year) else 'невисокосний'
    age = get_age(year)
    go_school = go_to_school(year)
    print(f"Ви народилися в {this_year} рік, "
          f"а в {go_school} році пішли до школи, зараз Вам {age} років."
          )


if __name__ == '__main__':
    about_you()
