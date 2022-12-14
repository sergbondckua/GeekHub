"""
Викорисовуючи Scrapy, написати скрипт, який буде приймати на вхід назву та
ID категорії (у форматі назва/id/) із сайту https://rozetka.com.ua і буде
збирати всі товари із цієї категорії, збирати всі можливі дані
(бренд, категорія, модель, ціна, рейтинг тощо) і зберігати їх у CSV файл
(наприклад, якщо передана категорія mobile-phones/c80003/, то файл буде
називатися c80003_products.csv)
"""
import json

# Scrapy
import scrapy
from scrapy.http import HtmlResponse


class RozetkaSpider(scrapy.Spider):
    """
    Scrape products from Rozetka
    """
    name = 'rozetka'
    allowed_domains = ['rozetka.com.ua']
    PAGE_URL = "https://rozetka.com.ua/api/product-api/v4/goods/" \
               "get-main?front-type=xl&country=UA&lang=ua&goodsId="

    def __init__(self, category=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [f"https://rozetka.com.ua/ua/{category}/"]

    def parse(self, response, **kwargs):
        """
        Parser all products from one page
        """
        for product_id in response.css(
                'ul.catalog-grid li.catalog-grid__cell div.g-id::text').getall():
            yield response.follow(self.PAGE_URL + product_id,
                                  callback=self.get_product,
                                  dont_filter=True)

        # Pagination pages
        number_of_pages = self.get_number_of_pages(response)
        for page_number in range(2, number_of_pages + 1):
            yield response.follow(f"{self.start_urls[0]}page={page_number}/",
                                  callback=self.parse)

    @staticmethod
    def get_number_of_pages(response: HtmlResponse) -> int:
        """
        Get the number of pages
        Args:
            :response: response HtmlResponse
            :return: number page
        """
        pagination = response.css(
            "a.pagination__direction--forward::attr(href)").get()
        if not pagination:
            return 1
        return int(pagination.split("=")[-1].strip("/"))

    @staticmethod
    def get_product(response: HtmlResponse):
        """
        Scrape product information
        """
        api = json.loads(response.text)
        item = {"id": api["data"]["id"],
                "title": api["data"]["title"],
                "old_price": api["data"]["old_price"],
                "price": api["data"]["price"],
                "href": api["data"]["href"],
                "brand": api["data"]["brand"],
                "category": api["data"]["last_category"]["title"]
                }

        yield item
