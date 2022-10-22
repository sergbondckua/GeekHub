"""
На основі попередньої функції (скопіюйте кусок коду) створити наступний скрипт:
   а) створити список із парами ім'я/пароль різноманітних видів
   (орієнтуйтесь по правилам своєї функції) - як валідні, так і ні;
   б) створити цикл, який пройдеться по цьому циклу і,
   користуючись валідатором, перевірить ці дані і надрукує для кожної
   пари значень відповідне повідомлення, наприклад:
      Name: vasya
      Password: wasd
      Status: password must have at least one digit
      -----
      Name: vasya
      Password: vasyapupkin2000
      Status: OK
   P.S. Не забудьте використати блок try/except ;)
"""


class NameLengthException(Exception):
    pass


class PasswdLengthException(Exception):
    pass


class NoDigitPasswdException(PasswdLengthException):
    pass


class UppercaseCharPasswdException(PasswdLengthException):
    pass


def validate_login_passwd(login, password):
    """ Validate login and password"""

    if 3 > len(login) or len(login) > 50:
        raise NameLengthException(
            "Login must be longer than 3 characters and no longer than 50"
        )
    if len(password) < 8:
        raise PasswdLengthException(
            "Password must be longer than 7 characters"
        )
    if not any([char.isdigit() for char in password]):
        raise NoDigitPasswdException("Password must have at least one digit")

    if not any([char.isupper() for char in password]):
        raise UppercaseCharPasswdException(
            f"Password must contain an uppercase letter"
        )
    return True


if __name__ == '__main__':
    username_long = 'u5_er' * 50

    access_data_list = {
        'us': 'password2A',
        username_long: 'password2A',
        'lorem': '5enQ',
        'dolor': 'wyerbcbrukck',
        'fish': 'jewjud3bfvvvd',
        'sergbond': 'CkUa1234#'

    }

    for name, passwd in access_data_list.items():
        try:
            validate_login_passwd(name, passwd)
        except NameLengthException as ex:
            print(
                f"Name: {name}\nPassword: {passwd}\n"
                f"Status: Name length problem")

        except NoDigitPasswdException as ex:
            print(f"Name: {name}\nPassword: {passwd}\nStatus: No digit passwd")

        except UppercaseCharPasswdException as ex:
            print(
                f"Name: {name}\nPassword: {passwd}\n"
                f"Status: No uppercase in password")

        except PasswdLengthException as ex:
            print(f"Name: {name}\nPassword: {passwd}\nStatus: Short password")

        else:
            print(f"Name: {name}\nPassword: {passwd}\nStatus: OK")
        finally:
            print('~' * 20)
