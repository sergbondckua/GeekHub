"""
Написати функцію, яка приймає два параметри:
ім'я (шлях) файлу та кількість символів. Файл також додайте в репозиторій.
На екран має бути виведений список із трьома блоками - символи з початку,
із середини та з кінця файлу. Кількість символів в блоках - та,
яка введена в другому параметрі. Придумайте самі, як обробляти помилку,
наприклад, коли кількість символів більша, ніж є в файлі або,
наприклад, файл із двох символів і треба вивести по одному символу,
то що виводити на місці середнього блоку символів?).
Не забудьте додати перевірку чи файл існує.
"""


def divided_blocks(filepath, amount):
    """Return list with three text blocks"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read().rstrip('\n')
        if amount > len(text):
            raise Exception("Amount is bigger than your file")
        left = text[:amount]
        right = text[-amount:]
        if amount % 2 == 0:
            center = text[(len(text) // 2 - amount // 2):(len(text) // 2 + amount // 2)]
        else:
            center = text[(len(text) // 2 - amount // 2):(len(text) // 2 + amount // 2 + 1)]
        print([left, center, right])
    except FileNotFoundError as e:
        print(e)


if __name__ == '__main__':
    divided_blocks('example.txt', 8)
