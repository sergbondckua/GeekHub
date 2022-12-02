"""
Cтворти клас RozetkaAPI, який буде містити 1 метод get_item_data,
який на вхід отримує id товара з сайту розетки та повертає словник з такими
даними: item_id (він же і приймається на вхід), title, old_price,
current_price,href (url на цей товар на сайті), brand, category.
Всі інші методи, що потрібні для роботи мають бути приватні/захищені.
"""
import logging
import time

import requests
from fake_useragent import UserAgent


class RozetkaAPI:  # pylint: disable=too-few-public-methods
    """Parser of the product by ID from Rozetka.ua"""

    _URL_API = "https://rozetka.com.ua/api/product-api/v4/goods/" \
               "get-main?front-type='xl&country=UA&lang=ua&goodsId="

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self.session = requests.Session()
        self.headers = {
            "User-Agent": UserAgent().random,
            "Accept": "application/json, text/plain, */*"
        }

    def get_item_data(self, id_product: str) -> tuple | bool:
        """Returns a tuple with product data
        :param id_product: product id
        :return: product data
        """
        url = self._URL_API + str(id_product)
        response = self.session.get(url, headers=self.headers, timeout=2)
        if response.status_code != 200:
            self._logger.error(
                "ID[%s] - Request failed with status code %s",
                id_product, response.status_code
            )
            time.sleep(0.5)
            return False

        item = response.json()
        product_data = (
            item["data"]["id"],
            item["data"]["title"],
            item["data"]["old_price"],
            item["data"]["price"],
            item["data"]["href"],
            item["data"]["brand"],
            item["data"]["last_category"]["title"],
        )
        return product_data
