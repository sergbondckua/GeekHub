"""
Напишіть сценарій, щоб перевірити, чи введене користувачем значення міститься в групі значень.
"""


def compare(value):
    if value in map(str, [1, 2, 'u', 'a', 4, True]):
        return True
    return False


if __name__ == '__main__':
    print(compare(input('Enter a value: ')))
