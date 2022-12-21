"""
Автоматизувати процес замовлення робота за допомогою Selenium
"""
import logging
import time
from pathlib import Path

# Selenium modules
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Chrome driver manager
from webdriver_manager.chrome import ChromeDriverManager

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)


class OrderedProcess:
    """Organization of automatic order"""
    _BASE_DIR = Path(__file__).resolve().parent
    _URL = "https://robotsparebinindustries.com/"
    __chromedriver = ChromeDriverManager().install()

    def __init__(self):
        self.logging = logging.getLogger(__name__)
        self.service = Service(self.__chromedriver)  # Service webdriver
        self.options = Options()  # Options webdriver
        # self.options.add_argument("--headless")  # Running in the background
        self.options.add_argument("--no-sandbox")  # Disable sandbox
        self.options.add_argument(
            "--disable-blink-features=AutomationControlled")  # To not detected
        self.browser = Chrome(service=self.service, options=self.options)

    def process_order(self):
        self.start_up()
        time.sleep(3)
    def start_up(self):
        """Start the Chrome browser"""
        self.browser.get(self._URL)

    def __enter__(self):
        self.start_up()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.browser.close()



if __name__ == '__main__':
    with OrderedProcess() as wa:
        wa.process_order()
