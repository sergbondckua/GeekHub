"""
Створіть функцію, всередині якої будуть записано СПИСОК із
п'яти користувачів (ім'я та пароль). Функція повинна приймати три аргументи: д
ва - обов'язкових (<username> та <password>) і третій
- необов'язковий параметр <silent> (значення за замовчуванням - <False>).
Логіка наступна:
    якщо введено правильну пару ім'я/пароль - вертається True;
    якщо введено неправильну пару ім'я/пароль:
        якщо silent == True - функція повертає False
        якщо silent == False - породжується виключення LoginException
        (його також треба створити =))

"""
import logging

logging.basicConfig(format="[%(levelname)s] - %(message)s")


class LoginException(Exception):
    pass


def check_access(username, password, silent=False):
    """ User validate"""
    access_data = [
        ("user_1", "passwd_1"),
        ("user_2", "passwd_2"),
        ("user_3", "passwd_3"),
        ("user_4", "passwd_4"),
        ("user_5", "passwd_5")
    ]
    for access in access_data:
        if (username, password) == (access[0], access[1]):
            return True
    if silent:
        return False
    else:
        raise LoginException("Wrong pair login / passwd, access denied")


if __name__ == '__main__':

    # First case
    try:
        check_access("user_1", "passwd_2")
    except LoginException as ex:
        logging.error(ex)
    else:
        print("First case: ", check_access("user_1", "passwd_2"))

    # Second case
    try:
        check_access("user_1", "passwd_2", True)
    except LoginException as ex:
        logging.error(ex)
    else:
        print("Second case: ", check_access("user_1", "passwd_2", True))

    # Third case
    try:
        check_access("user_1", "passwd_1", True)
    except LoginException as ex:
        logging.error(ex)
    else:
        print("Third case: ", check_access("user_1", "passwd_1", True))
