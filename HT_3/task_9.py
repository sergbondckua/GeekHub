""" Користувачем вводиться початковий і кінцевий рік. Створити цикл,
який виведе всі високосні роки в цьому проміжку (границі включно).
P.S. Рік є високосним, якщо він кратний 4,
але не кратний 100, а також якщо він кратний 400.
"""

start = int(input('Enter the start year: '))
end = int(input('Enter the end year: '))


def is_leap(year):
    leap_year = False
    if year % 4 == 0:
        leap_year = True
        if year % 100 == 0 and year % 400 != 0:
            leap_year = False
    return leap_year


leap_years_list = [year for year in range(start, end + 1) if is_leap(year)]
if leap_years_list:
    print('Leap years: ', leap_years_list)
else:
    print('***' * 3, f"{start} to {end} don't have leap years.", '***' * 3)
