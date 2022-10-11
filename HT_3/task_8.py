""" Створити цикл від 0 до ... (вводиться користувачем).
В циклі створити умову, яка буде виводити поточне значення, якщо остача від ділення на 17 дорівнює 0."""

list_multiple_of_17 = [i for i in range(1, int(input('Enter a number: '))) if i % 17 == 0]

print('\n'.join(map(str, list_multiple_of_17)))
