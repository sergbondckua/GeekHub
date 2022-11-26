"""
https://quotes.toscrape.com/ - написати скрепер для збору всієї доступної
інформації про записи: цитата, автор, інфа про автора тощо.
- збирається інформація з 10 сторінок сайту.
- зберігати зібрані дані у CSV файл
"""

import requests
import csv
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()
URL = "https://quotes.toscrape.com"

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
              "image/avif, image/webp,image/apng,"
              "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent": ua.random}


def get_author_about(url: str) -> list:
    link = url
    all_info = []
    s = requests.Session()
    while True:
        response = s.get(url=link, headers=headers)
        soup = BeautifulSoup(response.content, "lxml")
        quotes = soup.find_all("div", class_="quote")
        for num, quote in enumerate(quotes):
            text = quote.find_next("span", class_="text").text.strip()
            author = quote.find_next("small", class_="author").text.strip()
            about_link = url + quote.find_next("a").get("href")
            author_page = s.get(url=about_link, headers=headers)
            author_soup = BeautifulSoup(author_page.content, "lxml")
            born_date = author_soup.find(
                "span", class_="author-born-date").text.strip()
            born_place = author_soup.find(
                "span", class_="author-born-location"
            ).text.replace("in", "").strip()
            descript = author_soup.find(
                "div", class_="author-description").text.strip()

            # Generate list
            all_info.append(
                [num + 1, text, author, born_date, born_place, descript])
        if soup.find("li", class_="next"):
            page_link = soup.find("li", class_="next").find('a').get("href")
            link = url + page_link
        else:
            break

    # Save to file CSV
    with open("scraper.csv", "w") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(('Id', 'Name', 'DoB', 'Place', 'Description'))
        csv_writer.writerows(all_info)

    return all_info


def main():
    get_author_about(url=URL)


if __name__ == '__main__':
    main()
