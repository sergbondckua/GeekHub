"""
Напишіть сценарій для об’єднання наступних словників для створення НОВОГО.
"""

dict_1 = {'foo': 'bar', 'bar': 'buz'}
dict_2 = {'dou': 'jones', 'USD': 36}
dict_3 = {'AUD': 19.2, 'name': 'Tom'}

try:
    print(dict_1 | dict_2 | dict_3)
except TypeError:
    # Older versions of Python
    print({**dict_1, **dict_2, **dict_3})
