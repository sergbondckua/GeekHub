"""Parse the stream file CSV"""
import csv
import logging

import requests

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)


class Stream:
    """Getting data from a stream file CSV"""
    csv_url = "https://robotsparebinindustries.com/orders.csv"

    def __init__(self):
        self.logging = logging.getLogger(__name__)

    @property
    def get_data_csv(self):
        """Returns a CSV data in list format"""
        with requests.get(self.csv_url, stream=True, timeout=5) as response:
            lines = (line.decode('utf-8') for line in response.iter_lines())
            csv_data = list(csv.reader(lines))[1:]
        self.logging.info("Order file received. [<class 'list'>]")

        return csv_data

    @property
    def get_dict_csv(self):
        """Returns a CSV data in dict format"""
        with requests.get(self.csv_url, stream=True, timeout=5) as response:
            lines = (line.decode('utf-8') for line in response.iter_lines())
            csv_reader_dict = list(csv.DictReader(lines))
            csv_dict = [{k.replace(" ", "_").lower(): v}
                        for i in csv_reader_dict for k, v in i.items()]
        self.logging.info("Order file received. [<class 'dict'>]")

        return csv_dict
