"""
Головний модуль, який ініціалізує і запускає весь процес.
Суть процесу: читаємо ID товарів з csv файлу, отримуємо необхідні дані і
записуємо їх в базу. Якщо ID не валідний/немає даних - вивести відповідне
повідомлення і перейти до наступного.
"""

# Custom import
from rozetka_api import RozetkaAPI
from data_operations import CsvOperations, DataBaseOperations


def main():
    """Main function."""
    products_id = CsvOperations().get_data_file("util/id.csv")
    rozetka_api = RozetkaAPI().get_item_data
    all_products_data = [rozetka_api(id_product) for id_product in products_id
                         if rozetka_api(id_product)]
    DataBaseOperations().write_products_to_db(all_products_data)


if __name__ == '__main__':
    main()
