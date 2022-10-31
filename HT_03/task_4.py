""" Напишіть сценарій, який об’єднає три словники, оновивши ПЕРШИЙ
 (можна використовувати dicts з попереднього завдання)."""

dict_1 = {'foo': 'bar', 'bar': 'buz'}
dict_2 = {'dou': 'jones', 'USD': 36}
dict_3 = {'AUD': 19.2, 'name': 'Tom'}
dict_1.update(dict_2)
dict_1.update(dict_3)
print(dict_1)
