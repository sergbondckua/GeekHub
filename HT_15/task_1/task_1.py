"""
Викорисовуючи requests/BeautifulSoup, заходите на ось цей сайт
"https://www.expireddomains.net/domain-lists/" (з ним будьте обережні 😉 ☠),
вибираєте будь-яку на ваш вибір доменну зону і парсите список доменів з
усіма відповідними колонками - доменів там буде десятки тисяч
(звичайно ураховуючи пагінацію). Всі отримані значення зберегти в CSV файл.
"""
import csv
import logging
from time import sleep
from random import randint
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# Enable logging
logging.basicConfig(format="%(levelname)s - %(message)s",
                    level=logging.INFO)


class ParserDomains:
    """Scrape domain list"""

    _URL = "https://www.expireddomains.net/godaddy-most-active-domains/?start="

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()
        self.headers = {"Content-Type": "text/html; charset=UTF-8",
                        "User-Agent": UserAgent().random,
                        "Accept": "text/html,application/xhtml+xml,"
                                  "application/xml;q=0.9,image/avif,"
                                  "image/webp,image/apng,*/*;q=0.8,"
                                  "application/signed-exchange;v=b3;q=0.9"
                        }

    def get_all_statements(self) -> list:
        """Get all domain statements"""
        cnt_items = 0
        all_statements = []
        while True:
            if cnt_items >= 300:
                break
            self.session.headers.update(self.headers)
            response = self.session.get(self._URL + str(cnt_items), timeout=2)
            soup = BeautifulSoup(response.content, "lxml")
            all_statements.append(self._get_single_page_statements(soup))
            sleep(randint(4, 6))
            cnt_items += 25
            self.logger.info("%s items processed", cnt_items)
        return all_statements

    def _get_single_page_statements(self, soup: BeautifulSoup) -> [BeautifulSoup]:
        """Get single page statements"""
        domains = soup.find("table", class_="base1").find("tbody").find_all("tr")
        return [self._get_one_statement(domain) for domain in domains]

    @staticmethod
    def _get_one_statement(statement: BeautifulSoup) -> list:
        """Get one domain data"""
        dns = statement.find("td", class_="field_domain").find("a").text.strip()
        back_links = statement.find("td", class_="field_bl").find("a").text.strip()
        domain_pop = statement.find("td", class_="field_domainpop").find("a").text.strip()
        aby = statement.find("td", class_="field_abirth").text.strip()
        acr = statement.find("td", class_="field_aentries").find("a").text.strip()
        d_moz = statement.find("td", class_="field_dmoz").text.strip()
        com = statement.find("td", class_="field_statuscom").find("a").text.strip()
        net = statement.find("td", class_="field_statusnet").find("a").text.strip()
        org = statement.find("td", class_="field_statusorg").find("a").text.strip()
        de_zone = statement.find("td", class_="field_statusde").find("a").text.strip()
        reg = statement.find("td", class_="field_statustld_registered").text.strip()
        rdt = statement.find("td", class_="field_related_cnobi").text.strip()
        traffic = statement.find("td", class_="field_traffic").find("a").text.strip()
        valuation = statement.find("td", class_="field_valuation").find("a").text.strip()
        price = statement.find("td", class_="field_price").find("a").text.strip()
        bids = statement.find("td", class_="field_bids").find("a").text.strip()
        end_time = statement.find("td", class_="field_endtime").find("a").text.strip()

        return [dns, back_links, domain_pop, aby, acr, d_moz, com, net, org,
                de_zone, reg, rdt, traffic, valuation, price, bids, end_time]

    def write_products_to_csv(self) -> None:
        """Write statements to CSV file"""
        with open("domains.csv", "w", encoding="UTF-8") as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(
                ("Domain", "BL", "DP", "ABY", "ACR", "Dmoz", "C", "N", "O",
                 "D", "Reg", "RDT", "Traffic", "Valuation", "Price", "Bids",
                 "Endtime",))
            csv_writer.writerows(
                j for i in self.get_all_statements() for j in i)


def main():
    """Main function"""
    go_parser = ParserDomains()
    go_parser.write_products_to_csv()


if __name__ == '__main__':
    main()
