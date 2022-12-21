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

# Custom modules
from reader import Stream  # get stream file csv

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

class NotClosedException(Exception):
    """Unsuccessful attempt to close the browser"""


class OrderProcessPlacer:
    """Organization of automatic order
    Methods:
        :main_browser_process: General process
    """
    _BASE_DIR = Path(__file__).resolve().parent
    _URL = "https://robotsparebinindustries.com"
    __chromedriver = ChromeDriverManager().install()
    option_arguments = [
        "start-maximized",  # Opens Chrome in maximize mode
        #"--headless",  # Opens Chrome in background
        "--no-sandbox",  # Disable sandbox
        "--disable-blink-features=AutomationControlled",  # To not detected
        "disable-popup-blocking",  # Disables pop-ups displayed on Chrome
    ]

    def __init__(self):
        self.logging = logging.getLogger(__name__)
        self.service = Service(self.__chromedriver)  # Service webdriver
        self.options = Options()  # Options webdriver
        self.options.add_experimental_option(
            "excludeSwitches", ['enable-automation'])  # Disable info bar
        for argument in self.option_arguments:
            self.options.add_argument(argument)
        self.browser = Chrome(service=self.service, options=self.options)

    def main_process_order(self):
        """Starting a process ordering"""
        self.goto_order_bot()
        time.sleep(3)

    def start_up(self):
        """Start the Chrome browser"""
        self.logging.info(
            "Opening browser and visiting to URL: %s", self._URL)
        self.browser.get(self._URL)

    def status_element(self, by_element, timeout=5):
        """Wait for the element"""
        wait = WebDriverWait(self.browser, timeout)
        try:
            wait.until(EC.visibility_of_element_located(by_element))
        except TimeoutException as ex:
            raise TimeoutException('Not found element') from ex
    def goto_order_bot(self):
        """..."""
        self.logging.info("Go to order page")
        self.status_element((By.LINK_TEXT, "Order your robot!"))
        self.browser.find_element(By.LINK_TEXT, "Order your robot!").click()
        self.status_element((By.CLASS_NAME, "modal-content"))
        self.browser.find_element(By.CLASS_NAME, "btn-dark").click()

    def __enter__(self):
        self.start_up()  # open browser
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.browser.close()
            self.logging.info("Browser closed")
        except NotClosedException as error:
            self.logging.error("Error closing the web browser: %s", error)




if __name__ == '__main__':
    with OrderProcessPlacer() as opp:
        opp.main_process_order()
