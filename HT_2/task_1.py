"""
Напишіть сценарій, який приймає від користувача послідовність чисел, розділених комами,
і створює список і кортеж із цими числами.
"""

user_data_list = input('Enter numbers separated by commas: ').split(',')
user_data_tuple = tuple(user_data_list)
