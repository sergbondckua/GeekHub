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

ua = UserAgent()
URL = "https://quotes.toscrape.com"

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
              "image/avif, image/webp,image/apng,"
              "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent": ua.random}


def get_author_about(url: str) -> list:
    """Scrape quote and the author information"""
    link = url
    all_info = []
    num = 0
    session = requests.Session()
    while True:
        response = session.get(url=link, headers=headers)
        soup = BeautifulSoup(response.content, "lxml")
        quotes = soup.find_all("div", class_="quote")
        for quote in quotes:
            num += 1
            print("\r", f"Load {num}%", num * "#".rjust(1), end="")  # Loging
            text = quote.find_next("span", class_="text").text.strip('“”')
            author = quote.find_next("small", class_="author").text.strip()
            about_link = url + quote.find_next("a").get("href")
            author_page = session.get(url=about_link, headers=headers)
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
                [num, text, author, born_date, born_place, descript])
        if soup.find("li", class_="next"):
            page_link = soup.find("li", class_="next").find('a').get("href")
            link = url + page_link
        else:
            break

    return all_info


def main():
    """Main function"""
    all_info = get_author_about(URL)
    # Save to file CSV
    with open("scraper.csv", "w", encoding="UTF-8") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(
            ("Id", "Quote", "Name", "DoB", "Place", "Description"))
        csv_writer.writerows(all_info)


if __name__ == '__main__':
    main()
