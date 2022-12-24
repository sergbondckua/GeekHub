"""Automatically order the Robot"""

import os
import glob
import logging
from os import path
from pathlib import Path

# Selenium modules
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

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
    orders = Stream().get_dict_csv
    option_arguments = [
        "start-maximized",  # Opens Chrome in maximize mode
        # "--headless",  # Opens Chrome in background
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

    def start_up(self):
        """Start the Chrome browser"""
        self.logging.info(
            "Opening browser and visiting to URL: %s", self._URL)
        self.browser.get(self._URL)

    def main_process_order(self):
        """Starting a process ordering"""
        self._clear_folder()
        self.link_order_your_robot()
        self.modal_content_button()
        for order in self.orders:
            self.build_robot(order)
            self.button_preview()
            self.button_order()
            self.make_screenshot()
            self.logging.info(
                "🟢 #%s has been completed", order["order_number"])
            self.button_order_another()
            self.modal_content_button()
        self.logging.info("🏁 All orders is completed")

    def build_robot(self, data):
        """input values for build robot"""
        self.wait_element((By.TAG_NAME, "form"))
        self.head_select(data)
        self.body_input(data)
        self.legs_input(data)
        self.shipping_address(data)

    def wait_element(self, by_element, timeout=20):
        """Wait for the element"""
        wait = WebDriverWait(self.browser, timeout)
        try:
            element = wait.until(EC.visibility_of_element_located(by_element))
            return element
        except TimeoutException as ex:
            raise TimeoutException("Not found element") from ex

    def check_alert(self):
        """Check if the alert"""
        wait = WebDriverWait(self.browser, 2)
        try:
            wait.until(EC.visibility_of_element_located(
                (By.CLASS_NAME, "alert-danger")))
        except (TimeoutException, NoSuchElementException):
            return False
        alert = self.browser.find_element(By.CLASS_NAME, "alert").text
        self.logging.warning("A glitch has been detected: 🤬 <%s>", alert)
        return True

    def link_order_your_robot(self):
        """Page order bot"""
        self.wait_element((By.LINK_TEXT, "Order your robot!")).click()
        self.logging.info("Go to order page URL: %s", self.browser.current_url)

    def modal_content_button(self):
        """Press button OK"""
        self.wait_element((By.CLASS_NAME, "btn-dark")).click()

    def head_select(self, data):
        """Select a head for the robot"""
        Select(self.browser.find_element(
            By.ID, "head")).select_by_index(data["head"])

    def body_input(self, data):
        """Select a body for the robot"""
        self.browser.find_element(By.ID, f"id-body-{data['body']}").click()

    def legs_input(self, data):
        """Enter the part number for the legs"""
        legs = self.browser.find_element(
            By.CSS_SELECTOR,
            "input[placeholder='Enter the part number for the legs']")
        legs.clear()
        legs.send_keys(data["legs"])

    def shipping_address(self, data):
        """Shipping address"""
        address = self.browser.find_element(By.ID, "address")
        address.clear()
        address.send_keys(data["address"])

    def button_preview(self):
        """Press button Preview"""
        self.browser.find_element(By.ID, "preview").click()

    def button_order(self):
        """Press button Order"""
        order = self.browser.find_element(By.ID, "order")
        order.click()
        while self.check_alert():
            order.click()

    def button_order_another(self):
        """Press button Order Another Robot"""
        order_another = self.wait_element((By.ID, "order-another"))
        order_another.click()
        self.logging.info("➡️ Switching to another order")

    def get_receipt_id(self):
        """Get Receipt ID"""
        self.wait_element((By.ID, "receipt"))
        receipt_id = self.browser.find_element(
            By.ID, "receipt").find_element(By.TAG_NAME, "p").text
        return receipt_id

    def make_screenshot(self):
        """Make screenshot"""
        receipt = self.get_receipt_id()
        self.wait_element((By.ID, "robot-preview-image")).screenshot(
            path.join(self._BASE_DIR, f"output/{receipt}_robot.png"))
        self.logging.info("📸 Robot %s, photographed", receipt)

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
