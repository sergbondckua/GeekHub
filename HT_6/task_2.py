"""
Створіть функцію для валідації пари ім'я/пароль за наступними правилами:
   - ім'я повинно бути не меншим за 3 символа і не більшим за 50;
   - пароль повинен бути не меншим за 8 символів і повинен мати хоча б одну
   цифру;
   - якесь власне додаткове правило :)
Якщо якийсь із параметрів не відповідає вимогам
    - породити виключення із відповідним текстом.
"""
import logging

logging.basicConfig(format="[%(levelname)s] - %(message)s")


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
    while True:
        login = input("\nEnter username: ")
        passwd = input("\nEnter password: ")
        try:
            if not validate_login_passwd(login, passwd):
                pass
            print("\nCongratulations, all is good!")
            break
            
        except NameLengthException as ex:
            logging.warning(ex)
        except NoDigitPasswdException as ex:
            logging.warning(ex)
        except UppercaseCharPasswdException as ex:
            logging.warning(ex)
        except PasswdLengthException as ex:
            logging.warning(ex)
