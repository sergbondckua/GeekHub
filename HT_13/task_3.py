"""
Реалізуйте класс Transaction. Його конструктор повинен приймати такі параметри:

amount - суму на яку було здійснено транзакцію
date - дату переказу
currency - валюту в якій було зроблено переказ (за замовчуванням USD)
usd_conversion_rate - курс цієї валюти до долара (за замовчуванням 1.0)
description - опис транзакції (за дефолтом None)

Усі параметри повинні бути записані в захищені (_attr) однойменні атрибути.
Доступ до них повинен бути забезпечений лише на читання та за допомогою
механізму property. При чому якщо description дорівнює None,
то відповідне property має повертати рядок "No description provided".
Додатково реалізуйте властивість usd, що має повертати суму переказу у доларах
(сума * курс)
"""


class Transaction:
    def __init__(self,
                 amount: int,
                 date: str,
                 *,
                 currency="USD",
                 usd_conversion_rate: float = 1.0,
                 description=None):
        self._description = description
        self._usd_conversion_rate = usd_conversion_rate
        self._date = date
        self._currency = currency
        self._amount = amount

    @property
    def description(self) -> str:
        if not self._description:
            return "No description provided"
        return self._description

    @property
    def date(self):
        return self._date

    @property
    def currency(self):
        return self._currency

    @property
    def usd_conversion_rate(self) -> float:
        return self._usd_conversion_rate

    @property
    def currency(self):
        return self._currency

    @property
    def amount(self):
        return self._amount

    @property
    def usd(self) -> float:
        """Конвертація суми в USD"""
        return round(self._amount * self._usd_conversion_rate, 2)


if __name__ == '__main__':
    trans_1 = Transaction(4000, "23.11.2022", description="Donate 3CY")
    trans_2 = Transaction(4000, "23.11.2022", currency="UAH",
                          usd_conversion_rate=0.03756)

    for instance in (trans_1, trans_2):
        print(f"Сума переказу: {instance.amount} {instance.currency}\n"
              f"Дата: {instance.date}\n"
              f"Курс USD: {instance.usd_conversion_rate}\n"
              f"Призначення: {instance.description}\n"
              f"Сума в USD: ${instance.usd}\n" + 20 * "=+".center(2))
