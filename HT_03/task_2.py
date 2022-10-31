""" Напишіть сценарій для видалення порожніх елементів зі списку."""

test_list = [
    (), 'hey', ('',), ('ma', 'ke', 'my'), [''], {}, ['d', 'a', 'y'], '', []
]
print([item for item in test_list if item])
