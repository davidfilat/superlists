import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

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

    def setUp(self):
        self.browser = self.set_browser()

        staging_server = os.environ.get("STAGING_SERVER")
        if staging_server:
            self.live_server_url = staging_server

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id("id_list_table")
                rows = table.find_elements_by_tag_name("tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def wait_for(self, fn):
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def get_item_input_box(self):
        return self.browser.find_element_by_id("id_text")
