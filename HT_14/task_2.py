"""
Створіть програму для отримання курсу валют за певний період.
- отримати від користувача дату (це може бути як один день так і
інтервал - початкова і кінцева дати, продумайте механізм реалізації)
і назву валюти
- вивести курс по відношенню до гривні на момент вказаної дати
(або за кожен день у вказаному інтервалі)
- не забудьте перевірку на валідність введених даних
"""

import requests
from datetime import datetime, timedelta


class CurrencyView:
    __url = "https://bank.gov.ua/NBU_Exchange/exchange?json&date="
    __codes = ['USD', 'UZS', 'GEL', 'AUD', 'AZN', 'BYN', 'CAD', 'CHF', 'CNY',
               'CZK', 'DKK', 'EUR', 'GBP', 'HUF', 'ILS', 'JPY', 'KZT', 'MDL',
               'NOK', 'PLN', 'SEK', 'SGD', 'TMT', 'TRY']

    def __init__(self,
                 currency: str,
                 start_date: datetime,
                 end_date: datetime):
        self.start = start_date
        self.end = end_date
        self.currency = currency

    @property
    def currency(self):
        return self._currency

    @currency.setter
    def currency(self, value):
        if value not in self.__codes:
            raise Exception("Currency not supported")
        self._currency = value

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value: datetime):
        if not datetime(1996, 2, 1) <= value <= datetime.now():
            raise Exception("Wrong period or date")
        self._start = value

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value: datetime):
        if not self._start <= value <= datetime.now():
            raise Exception("Wrong period or date")
        self._end = value

    @property
    def get_period_currency(self) -> list:
        """Return selected currency rate"""

        date_list = [self._start + timedelta(days=x)
                     for x in range((self.end - self._start).days + 1)]
        result = []
        for day in date_list:
            response = requests.get(self.__url + day.strftime("%d%m%Y"))
            data = response.json()
            result.append({day.date().strftime("%d.%m.%Y"): {
                "currency": self._currency,
                "rate": i["Amount"],
                "units": i["Units"]}
                for i in data if i["CurrencyCodeL"] == self._currency})
        return result


if __name__ == '__main__':

    try:
        period = input("Enter the date in the format dd.mm.yyyy.\n"
                       "Examples: 01.12.2014\n or\n"
                       "Data of range: 01.12.2014-05.12.2014:\n").split("-")
        start = datetime.strptime(period[0].strip(), "%d.%m.%Y")
        end = datetime.strptime(period[1].strip(), "%d.%m.%Y")\
            if len(period) > 1 else start
        curr = input("Enter the currency: ").upper().strip()
        view = CurrencyView(curr, start, end).get_period_currency
        print(view)
    except ValueError as ex:
        print(ex)
