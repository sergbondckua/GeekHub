""" Напишіть сценарій для видалення дублікатів значень зі словника. Не соромтеся жорстко кодувати свій словник."""

dict_with_duplicates = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 1, 'J': 2, 'K': 3, 'L': 4, 'M': 5}
dict_without_duplicates = {}

for key, value in dict_with_duplicates.items():
    if value in dict_without_duplicates.values():
        continue
    dict_without_duplicates[key] = value

print(dict_without_duplicates)
