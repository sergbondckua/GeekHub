"""Scrapes"""
import os
import sys
import logging
import time

import django
import requests
from fake_useragent import UserAgent

sys.path.append(os.path.dirname(os.path.abspath("scrape")))
os.environ["DJANGO_SETTINGS_MODULE"] = "app.settings"
django.setup()

from rozetka.models import ScrapingTask, Product


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

    def get_item_data(self, id_product: str) -> dict | bool:
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
        product_data = {
            "id": item["data"]["id"],
            "title": item["data"]["title"],
            "old_price": item["data"]["old_price"],
            "price": item["data"]["price"],
            "href": item["data"]["href"],
            "brand": item["data"]["brand"],
            "category": item["data"]["last_category"]["title"],
            "description": item["data"]["description"]["text"]
        }
        return product_data


class DataBaseOperations:  # pylint: disable=too-few-public-methods
    """Operations with the SQLite database"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def write_products_to_db(self, scrape_list: list) -> None:
        """Write products to the database"""
        objs = [Product(
            product_id=product["id"],
            title=product["title"],
            old_price=product["old_price"],
            price=product["price"],
            href=product["href"],
            brand=product["brand"],
            category=product["category"],
            description=product["description"],
        ) for product in scrape_list]
        Product.objects.bulk_create(objs)


def main():
    """Main function"""
    tasks = ScrapingTask.objects.get(id=sys.argv[1]).products_id.split("\n")
    list_tasks = [task.strip("\r") for task in tasks]
    api = RozetkaAPI().get_item_data
    all_products_data = [api(pid) for pid in list_tasks if api(pid)]
    ScrapingTask.objects.get(id=sys.argv[1]).delete()
    DataBaseOperations().write_products_to_db(all_products_data)


if __name__ == '__main__':
    main()
