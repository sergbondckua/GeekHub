"""
Write a script which accepts a <number> from user and then <number> times asks user for string input.
At the end script must print out result of concatenating all <number> strings.
"""

concatenating = ''
for _ in range(int(input('Enter a number: '))):
    concatenating += input('Type something...: ')

print(concatenating)
