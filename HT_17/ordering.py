"""Automatically order the Robot"""
import glob
import logging
import os
from os import path
from pathlib import Path

# Selenium modules
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

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
        :start_up: Start up browser
        :status_element: Wait condition element
        :goto_order_bot: Go to page Order
        :check_alert: Check glitch
        :input_order_fields: Checkout process
        :make_screenshot: Make screenshot
        :_clear_folder: Clear all files in folder
    """
    _BASE_DIR = Path(__file__).resolve().parent
    _URL = "https://robotsparebinindustries.com"
    __chromedriver = ChromeDriverManager().install()
    orders = Stream().get_data_csv
    option_arguments = [
        "start-maximized",  # Opens Chrome in maximize mode
        "--headless",  # Opens Chrome in background
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
        self._clear_folder()
        self.goto_order_bot()
        self.input_order_fields()

    def start_up(self):
        """Start the Chrome browser"""
        self.logging.info(
            "Opening browser and visiting to URL: %s", self._URL)
        self.browser.get(self._URL)

    def status_element(self, by_element, timeout=20):
        """Wait for the element"""
        wait = WebDriverWait(self.browser, timeout)
        try:
            wait.until(EC.visibility_of_all_elements_located(by_element))
        except TimeoutException as ex:
            raise TimeoutException('Not found element') from ex


    def goto_order_bot(self):
        """Page order bot"""
        self.logging.info("Go to order page")
        self.status_element((By.LINK_TEXT, "Order your robot!"))
        self.browser.find_element(By.LINK_TEXT, "Order your robot!").click()
        self.status_element((By.CLASS_NAME, "modal-content"))
        self.browser.find_element(By.CLASS_NAME, "btn-dark").click()

    def check_alert(self):
        """Check if the alert"""
        wait = WebDriverWait(self.browser, 3)
        try:
            wait.until(EC.visibility_of_element_located(
                (By.CLASS_NAME, "alert-danger")))
        except (TimeoutException, NoSuchElementException):
            return False
        alert = self.browser.find_element(By.CLASS_NAME, "alert").text
        self.logging.warning("A glitch has been detected: <%s>", alert)
        return True

    def input_order_fields(self):
        """Enter fields form"""
        for num, _ in enumerate(self.orders):
            self.status_element((By.TAG_NAME, "form"))
            order = self.browser.find_element(By.ID, "order")
            # Select head
            head = Select(self.browser.find_element(By.ID, "head"))
            head.select_by_index(self.orders[num][1])
            # Check radio body
            body = self.browser.find_element(
                By.ID, f"id-body-{self.orders[num][1]}")
            body.click()
            # Input legs
            legs = self.browser.find_element(
                By.XPATH,
                '//*[@placeholder="Enter the part number for the legs"]')
            legs.clear()
            legs.send_keys(self.orders[num][3])
            # Input address
            address = self.browser.find_element(By.ID, "address")
            address.clear()
            address.send_keys(self.orders[num][4])
            # Press button Preview
            preview = self.browser.find_element(By.ID, "preview")
            preview.click()
            self.status_element(
                (By.XPATH, '//*[@id="robot-preview-image"]/img[3]'))
            # press button Order
            order.click()
            # Click until the glitch disappears
            while self.check_alert():
                order.click()
            self.status_element((By.ID, "receipt"))
            receipt_id = self.browser.find_element(
                By.ID, "receipt").find_element(By.TAG_NAME, "p")
            self.status_element(
                (By.XPATH, '//*[@id="robot-preview-image"]/img[3]'))
            # Make screenshot
            self.make_screenshot(receipt_id)
            self.status_element((By.ID, "order-another"))
            self.browser.find_element(By.ID, "order-another").click()
            self.status_element((By.CLASS_NAME, "modal-content"))
            self.browser.find_element(By.CLASS_NAME, "btn-dark").click()
            self.logging.info("[%s]. Robot has been completed", num)

    def make_screenshot(self, receipt_id):
        """Make screenshot"""
        self.browser.find_element(
            By.ID, "robot-preview-image").screenshot(
            path.join(self._BASE_DIR, f"output/{receipt_id.text}_robot.png"))
        self.logging.info("Robot %s, photographed", receipt_id.text)

    def _clear_folder(self):
        """Deleted all files in the folder"""
        for file in glob.glob(path.join(self._BASE_DIR, "output/*")):
            os.remove(file)
        self.logging.info("The folder has been cleared.")

    def __enter__(self):
        self.start_up()  # open browser
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.browser.close()
            self.logging.info("Browser closed")
        except NotClosedException as error:
            self.logging.error("Error closing the web browser: %s", error)
