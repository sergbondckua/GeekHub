"""
Напишіть сценарій, який приймає від користувача дві послідовності кольорів, розділених комами.
Потім роздрукуйте набір, що містить усі кольори з color_list_1, яких немає в color_list_2.
"""

color_list_1 = set(input('Enter the first list of colors separated by commas: ').split(','))
color_list_2 = set(input('Enter a second list of colors separated by commas: ').split(','))

print(color_list_1 - color_list_2)

