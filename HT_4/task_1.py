"""
Написати функцiю season, яка приймає один аргумент (номер мiсяця вiд 1 до 12)
та яка буде повертати пору року,
до якої цей мiсяць належить (зима, весна, лiто або осiнь).
У випадку некоректного введеного значення - виводити відповідне повідомлення.
"""


def get_season(month):
    """Returns the season"""

    months_of_year = dict(
        Winter=(1, 2, 12),
        Spring=(3, 4, 5),
        Summer=(6, 7, 8),
        Autumn=(9, 10, 11)
    )

    if month in range(1, 13):
        for season_name, value in months_of_year.items():
            if month in value:
                return season_name
    else:
        print('Invalid input, only numbers 1 to 12.')

    return get_season(int(input('Try again:\n')))


if __name__ == '__main__':
    number_month = int(input('Enter month number, only numbers 1 to 12:\n'))
    print(get_season(number_month))
