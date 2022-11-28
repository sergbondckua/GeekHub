"""
https://quotes.toscrape.com/ - написати скрепер для збору всієї доступної
інформації про записи: цитата, автор, інформація про автора тощо.
- збирається інформація з 10 сторінок сайту.
- зберігати зібрані дані у CSV файл
"""
import csv
import requests

from bs4 import BeautifulSoup
from fake_useragent import UserAgent


class Parser:
    """Parser requests"""
    ua = UserAgent()
    URL = "https://quotes.toscrape.com"

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
                  "image/avif, image/webp,image/apng,"
                  "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": ua.random}

    def get_all_info(self) -> list:
        """Returns all information of the product"""
        all_info = []
        link = self.URL
        num = 0
        while True:
            num += 1
            print("\r", f"Load {num} pages", num * "#".rjust(1), end="")  # Loging
            page = requests.get(link, headers=self.headers, timeout=10)
            soup = BeautifulSoup(page.content, "lxml")
            all_info.extend(self.get_one_page_quotes(soup))
            if soup.find("li", class_="next"):
                next_page_link = soup.find("li", class_="next").find("a").get("href")
                link = self.URL + next_page_link
            else:
                break

        return all_info

    def get_one_page_quotes(self, soup_quotes: BeautifulSoup) -> list:
        """Returns all the quotes in a given"""
        quotes = soup_quotes.find_all("div", class_="quote")
        return [self.get_one_quote(quote) for quote in quotes]

    def get_one_quote(self, soup_quote: BeautifulSoup) -> list:
        """Returns one quote"""
        text = soup_quote.find_next("span", class_="text").text.strip('“”')
        author = soup_quote.find_next("small", class_="author").text.strip()
        about_link = self.URL + soup_quote.find_next("a").get("href")
        author_page = requests.get(about_link, headers=self.headers, timeout=10)
        author_soup = BeautifulSoup(author_page.content, "lxml")
        born_date = author_soup.find(
            "span", class_="author-born-date").text.strip()
        born_place = author_soup.find(
            "span", class_="author-born-location"
        ).text.replace("in", "").strip()
        descript = author_soup.find(
            "div", class_="author-description").text.strip()
        return [text, author, born_date, born_place, descript]

    @staticmethod
    def write_products_to_csv(result_data: list) -> None:
        """Write the information about"""
        with open("scraper.csv", "w", encoding="UTF-8") as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(
                ("Id", "Quote", "Name", "DoB", "Place", "Description"))
            csv_writer.writerows(result_data)


def main():
    """Main function"""
    parser = Parser()
    result_data = parser.get_all_info()
    parser.write_products_to_csv(result_data)


if __name__ == '__main__':
    main()
