"""Scrape Vikka.ua"""
import logging
from datetime import datetime

from scrapy import Spider, Selector
from scrapy.http.response.html import HtmlResponse

# Enable logging
logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.ERROR)
logging = logging.getLogger(__name__)


def start_page() -> str:
    """Return start_page
    Returns:
        str: start page"""
    while True:
        date = input("What date to show the news feed?\n"
                     "Enter date (Format: dd.mm.yyyy): ")
        try:
            page = datetime.strptime(date, '%d.%m.%Y')
            if page <= datetime.now():
                return page.strftime("%Y/%m/%d")
            logging.error("It is impossible to receive news from the future.")
        except ValueError:
            logging.error(
                "Invalid date %s or does not match format 'dd.mm.yyyy'", date)


class VikkaNewsSpider(Spider):
    """Scrape the news feed from 'Vikka.ua'"""
    name = "vikka_news"
    allowed_domains = ["vikka.ua"]
    news_date = start_page()
    start_urls = [f"https://www.vikka.ua/{news_date}/"]
    # Save the news feed to CSV file and json file
    custom_settings = {
        "FEEDS": {
            f"out_files/csv/{news_date.replace('/', '_')}.csv": {  # CSV
                "format": "csv",
                "header": True,
                "encoding": "utf-8",
                "indent": True,
                "overwrite": True},
            f"out_files/json/{news_date.replace('/', '_')}.json": {  # JSON
                "format": "json",
                "encoding": "utf-8",
                "escape": False,
                "newline": "",
                "ensure_ascii": False,
                "indent": 4,
                "overwrite": True},
        }
    }

    def parse(self, response, **kwargs):
        """
        Parse the news feed
        Args:
            response: response object
        """
        # All items in the one page
        for news_item in response.css("div.content-area li"):
            link = news_item.css("a.more-link-style::attr(href)").get()
            if link:
                yield response.follow(
                    link, callback=self.parse_article, dont_filter=True)

        # Pagination pages
        number_of_pages = self.get_number_of_pages(response)
        for page_number in range(2, number_of_pages + 1):
            yield response.follow(
                f"{self.start_urls[0]}page/{page_number}/",
                callback=self.parse, dont_filter=True)

    @staticmethod
    def get_number_of_pages(response: HtmlResponse) -> int:
        """
        Get the number of pages
        Args:
            :response: response object
            :return: number page"""
        pagination = response.css("a.next::attr(href)").get()
        if not pagination:
            return 1
        return int(pagination.split("/")[-2])

    @staticmethod
    def parse_article(response: HtmlResponse):
        """
        Parse the article
        Args:
            response: response object"""
        items = {
            "time_pub": response.css(
                "span.post-info-style::text").get().split(",")[1].strip(),
            "title": response.css("h1::text").get().strip(),
            "text": "".join([text.replace('”', "'").replace(
                '“', "'").replace(" ", " ") for text in response.css(
                "div.entry-content *::text").getall()[:-2]]),
            "tags": ", ".join(
                ["#" + tag.strip().replace(" ", "_") for tag in response.css(
                    "div.entry-tags a::text").getall()]), "url": response.url,
        }

        yield items
