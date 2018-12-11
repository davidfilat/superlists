import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

from functional_tests.server_tools import reset_database

MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):
    @staticmethod
    def set_browser(browser="chrome"):
        driver = None
        if browser == "firefox":
            from selenium.webdriver.firefox.options import Options

            firefox_options = Options()
            firefox_options.add_argument("-headless")
            try:
                driver = webdriver.Firefox(firefox_options=firefox_options)
            except WebDriverException:
                driver = webdriver.Firefox(
                    "/usr/local/bin/geckodriver", firefox_options=firefox_options
                )

        elif browser == "chrome":
            from selenium.webdriver.chrome.options import Options

            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--window-size=1920x1080")
            try:
                driver = webdriver.Chrome(chrome_options=chrome_options)
            except WebDriverException:
                driver = webdriver.Chrome(
                    "/usr/local/bin/chromedriver", chrome_options=chrome_options
                )

        elif browser == "safari":
            driver = webdriver.Safari()
        return driver

    def wait(fn):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            while True:
                try:
                    return fn(*args, **kwargs)
                except (AssertionError, WebDriverException) as e:
                    if time.time() - start_time > MAX_WAIT:
                        raise e
                    time.sleep((0.5))

        return wrapper

    def setUp(self):
        self.browser = self.set_browser()

        self.staging_server = os.environ.get("STAGING_SERVER")
        if self.staging_server:
            self.live_server_url = self.staging_server
            reset_database()

    def tearDown(self):
        self.browser.quit()

    @wait
    def wait_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertIn(row_text, [row.text for row in rows])
        return

    @wait
    def wait_for(self, fn):
        return fn()

    def get_item_input_box(self):
        return self.browser.find_element_by_id("id_text")

    @wait
    def wait_to_be_logged_in(self, email):
        self.browser.find_element_by_link_text("Log out")
        navbar = self.browser.find_element_by_css_selector(".navbar")
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email):
        self.browser.find_element_by_name("email")
        navbar = self.browser.find_element_by_css_selector(".navbar")
        self.assertNotIn(email, navbar.text)


def add_list_item(self, item_text):
    num_rows = len(self.browser.find_elements_by_css_selector("#id_list_table tr"))
    self.get_item_input_box().send_keys(item_text)
    self.get_item_input_box().send_keys(Keys.ENTER)
    item_number = num_rows + 1
    self.wait_for_row_in_list_table(f"{item_number}: {item_text}")
