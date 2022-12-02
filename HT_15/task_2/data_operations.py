"""
Класами CsvOperations та DataBaseOperations.
CsvOperations містить метод для читання даних.
Метод для читання приймає аргументом шлях до csv файлу де в колонкі ID записані
як валідні, так і не валідні id товарів з сайту.
DataBaseOperations містить метод для запису даних в sqlite3 базу і відповідно
приймає дані для запису. Всі інші методи, що потрібні для роботи мають бути
приватні/захищені.
"""
import csv
import logging
import sqlite3

# Enable logging
logging.basicConfig(format="%(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO)


class CsvOperations:  # pylint: disable=too-few-public-methods
    """Operations with the CSV files"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_data_file(self, path: str) -> list[str]:
        """
        Get id's from the given path.
        :param path: path to the CSV file
        :return: list of ids.
        """
        with open(path, 'r', encoding="UTF-8") as csvfile:
            self.logger.info("Reading file %s", path)
            reader = csv.DictReader(csvfile)
            return [row['ID'] for row in reader]


class DataBaseOperations:  # pylint: disable=too-few-public-methods
    """Operations with the SQLite database"""

    _connect_sql = sqlite3.connect("util/rozetka.db")
    with _connect_sql:
        _cursor = _connect_sql.cursor()

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def write_products_to_db(self, products: list) -> None:
        """Write products to the database"""
        try:
            self.logger.info("Writing products to DB")
            with self._connect_sql:
                self._cursor.executemany(
                    """INSERT INTO products
                    (product_id,
                    title,
                    old_price,
                    price,
                    href,
                    brand,
                    category)
                    VALUES (?,?,?,?,?,?,?)
                    ON CONFLICT(product_id) DO UPDATE SET
                    product_id = product_id,
                    title = title,
                    old_price = old_price,
                    price = price,
                    href = href,
                    brand = brand""", products)
                self._connect_sql.commit()
                self.logger.info("All products have been saved successfully")
        except sqlite3.Error as error:
            self.logger.error(error)
            self._connect_sql.rollback()
