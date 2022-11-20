"""
Створіть за допомогою класів та продемонструйте свою реалізацію
шкільної бібліотеки (включіть фантазію).
Наприклад вона може містити класи:
Person, Teacher, Student, Book, Shelf, Author, Category і.т.д.
Можна робити по прикладу банкомату з меню, базою даних і т.д.
"""
import sqlite3
from abc import ABC, abstractmethod


class SqlConfig:
    """SQL налаштування"""
    conn = sqlite3.connect('library.db')
    with conn:
        cursor = conn.cursor()


class Book(SqlConfig):
    _role = "student"

    def __init__(self, title, author: str):
        self.author = author
        self.title = title


class Textbook(Book):
    """Підручник"""

    def __init__(self, title: str, author: str, for_class: int):
        super().__init__(title, author)
        self.for_class = for_class

    def add(self):
        """Додає підручник до бібліотеки"""
        with self.conn:
            self.cursor.execute(
                """INSERT INTO books (title, autor, category, count)
                    VALUES (?,?,?,?)""",
                (self.title, self.author, self.for_class, 1))
            self.conn.commit()
            print("Textbook:", self.title, self.author, self.for_class,
                  "Add success")


class Magazine(Book):
    """Журнал"""

    def __init__(self, title: str, author: str, public_year: int):
        super().__init__(title, author)
        self.public_year = public_year

    def add(self):
        """Додає журнал до бібліотеки"""
        with self.conn:
            self.cursor.execute(
                """INSERT INTO books (title, autor, category, count)
                    VALUES (?,?,?,?)""",
                (self.title, self.author, self.public_year, 1))
            self.conn.commit()
            print("Magazine:", self.title, self.author, self.public_year,
                  "Add success")


class FeedbackMixin:
    """Записує відгук про бібліотеку"""

    @staticmethod
    def add_feedback(text: str) -> str:
        print(f"Your feedback: {text}")
        return text


class Person(ABC, SqlConfig):
    """ Базовий клас"""
    _role = "student"

    def __init__(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name

    def view(self):
        """Повертає всі видання, які в наявності"""
        return self.cursor.execute(
            "SELECT * FROM books WHERE count > 0").fetchall()

    @abstractmethod
    def print_info(self):
        """Інформація про персону"""
        pass


class Teacher(Person, SqlConfig):
    __role = "teacher"

    def __init__(self, first_name: str, last_name: str, subject: str):
        super().__init__(first_name, last_name)
        self.subject = subject

    def print_info(self) -> tuple:
        print(f"{self.subject} {self.__role}: ",
              self.first_name, self.last_name)
        return self.first_name, self.last_name, self.__role

    def take(self, id_edition: int) -> tuple:
        """Повертає обранє видання"""
        try:
            print(f"Issued by: {self.view()[id_edition - 1]}")
            return self.view()[id_edition - 1]
        except IndexError:
            print("Not found the edition")


class Student(Person, FeedbackMixin):
    def __init__(self, first_name: str, last_name: str, study_class: int):
        super().__init__(first_name, last_name)
        self.study_class = study_class

    def view(self):
        """Повертає всі видання"""
        return self.cursor.execute(
            "SELECT * FROM books WHERE category = ? AND count > 0",
            (self.study_class,)).fetchall()

    def take(self, id_textbook: int) -> tuple:
        """Повертає обраний підручник"""
        try:
            print(f"Issued by: {self.view()[id_textbook - 1]}")
            return self.view()[id_textbook - 1]
        except IndexError:
            print("Not found book")

    def print_info(self) -> tuple:
        print(f"{self.study_class}-th grade {self._role}: ",
              self.first_name, self.last_name)

        return self.first_name, self.last_name, self._role


class Staff(Person):
    __role = "staff"

    def view(self):
        """Повертає всі видання"""
        return self.cursor.execute("SELECT * FROM books").fetchall()

    def add_textbook(self, title: str, author: str, for_class: int):
        """Додає підручник в бд"""
        if self.__role == "staff":
            Textbook(title, author, for_class).add()
        else:
            print("not allowed...")

    def add_magazine(self, title: str, author: str, public_year: int):
        """Додає журнал в бд"""
        if self.__role == "staff":
            Magazine(title, author, public_year).add()
        else:
            print("not allowed...")

    def print_info(self) -> tuple:
        print(f"{self.__role}: ",
              self.first_name, self.last_name)
        return self.first_name, self.last_name, self.__role


# Staff
librarian = Staff("John", "Smith")  # Бібліотекар Джон Сміт
librarian.print_info()  # Інформація про працівника
librarian.add_textbook("Algebra", "Edgar Po", 7)  # Додає підручник
librarian.add_magazine("Murzilka", "Kiev-print ltd.", 2022)  # Додає журнал
print(librarian.view())  # Всі видання в бібліотеці

print(40 * "#".center(2), "\n")

# Student
student = Student("Carl", "Fox", 5)  # Карл Фокс, 5-й клас
student.print_info()  # Інформація про учня
print(student.view())  # Підручники, для 5-го класу
student.take(1)  # Взяти обраний підручник з бібліотеки
student.add_feedback("Good feedback for employees")  # Залишає відгук

print(40 * "#".center(2), "\n")

# Teacher
teacher = Teacher("Mary", "Jane", "History")  # Вчителька історії, Марі Джейн
teacher.print_info()  # Інформація про вчителя
print(student.view())  # Видання, для вчителів
teacher.take(4)  # Взяти обранє з бібліотеки
