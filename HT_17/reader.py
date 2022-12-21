"""Parse the stream file CSV"""
import csv
import requests

class Stream:
    """Getting data from a stream file CSV"""
    csv_url = "https://robotsparebinindustries.com/orders.csv"
    @property
    def get_data_csv(self):
        """Returns a CSV data"""

        with requests.get(self.csv_url, stream=True, timeout=1) as response:
            lines = (line.decode('utf-8') for line in response.iter_lines())
            data_csv = list(csv.reader(lines))[1:]
        return data_csv
