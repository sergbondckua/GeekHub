"""Використовуючи Scrapy,
заходите на "https://chrome.google.com/webstore/sitemap"
переходите на кожен лінк з тегів <loc>, з кожного лінка берете посилання на
сторінки екстеншинів, парсите їх і зберігаєте в CSV файл ID, назву та короткий
пис кожного екстеншена (пошукайте уважно де його можна взяти).
Наприклад:
“aapbdbdomjkkjkaonfhkkikfgjllcleb”,
“Google Translate”,
“View translations easily as you browse the web. By the Google Translate team.”
"""
import re

import scrapy
from scrapy.http.response.html import HtmlResponse

class ChromegoogleSpider(scrapy.Spider):
    """Scrape the extensions of Chrome"""
    name = "chromegoogle"
    allowed_domains = ["chrome.google.com"]
    start_urls = ["https://chrome.google.com/webstore/sitemap"]

    def parse(self, response: HtmlResponse, **kwargs):
        """
        Parse all the links in the response
        :param response: HtmlResponse
        """
        for link in response.xpath("//*[local-name()='loc']/text()").getall():
            if link:
                yield response.follow(
                    link, callback=self.parse_sub_links, dont_filter=True)
    def parse_sub_links(self, response: HtmlResponse):
        """
        Parse all sub_links in response
        :param: response: HtmlResponse
        """
        for sub_link in response.xpath(
                "//*[local-name()='loc']/text()").getall():
            yield response.follow(
                sub_link, callback=self.parse_extension, dont_filter=True)

    @staticmethod
    def parse_extension(response:HtmlResponse):
        """
        Parse a extensions
        :param: response: HtmlResponse
        """
        item = {
            "id": re.findall(
                r"(^\w+)", response.url.split("/")[-1].strip())[0],
            "name": response.css("h1::text").get().strip(),
            "description": response.css(
                "div.C-b-p-j-Pb::text").get().replace("\n", " ")
        }
        yield item
