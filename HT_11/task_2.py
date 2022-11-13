"""
Створити клас Person, в якому буде присутнім метод __init__ який буде приймати
якісь аргументи, які зберігатиме в відповідні змінні.
- Методи, які повинні бути в класі Person - show_age, print_name,
show_all_information.
- Створіть 2 екземпляри класу Person та в кожному з екземплярів створіть
атрибут profession (його не має інсувати під час ініціалізації в самому класі)
та виведіть його на екран (прінтоніть)
"""


class Person:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def show_age(self):
        return self.age

    def print_name(self):
        return self.name

    def show_all_information(self):
        return self.__dict__


if __name__ == '__main__':
    human = Person("John Dou", 30)
    human2 = Person("Will Smith", 50)

    human.profession = "Project Manager"
    human2.profession = "HR Generalist"

    print(human.show_all_information())
    print(human2.show_all_information())
