import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):
    @staticmethod
    def set_browser():
        CHROME_DRIVER = os.environ.get("CHROME_DRIVER")
        GECKODRIVER = os.environ.get("GECKODRIVER")
        if CHROME_DRIVER:
            from selenium.webdriver.chrome.options import Options

            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--window-size=1920x1080")
            return webdriver.Chrome(
                chrome_options=chrome_options, executable_path=CHROME_DRIVER
            )
        elif GECKODRIVER:
            return webdriver.Firefox(executable_path=GECKODRIVER)
        else:
            return webdriver.Firefox()

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
