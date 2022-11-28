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
        page = requests.get(self.URL, headers=self.headers, timeout=1)
        start_page_soup = BeautifulSoup(page.content, 'lxml')
        print("Start parser:")
        all_info = self.get_one_page_quotes(start_page_soup)
        for num_pages in range(2, 11):
            print("\r", f"Load {num_pages} pages", num_pages * "#".rjust(1), end="")  # Loging
            page = requests.get(self.URL + f"/page/{num_pages}", headers=self.headers, timeout=10)
            soup = BeautifulSoup(page.content, "lxml")
            all_info.extend(self.get_one_page_quotes(soup))

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
                ("Quote", "Name", "DoB", "Place", "Description"))
            csv_writer.writerows(result_data)


def main():
    """Main function"""
    parser = Parser()
    result_data = parser.get_all_info()
    parser.write_products_to_csv(result_data)


if __name__ == '__main__':
    main()
