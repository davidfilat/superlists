import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
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
                time.sleep(5)

    def setUp(self):
        self.browser = webdriver.Firefox(executable_path="/usr/local/bin/geckodriver")

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrive_it_later(self):
        # Browser opens the main page
        self.browser.get(self.live_server_url)

        # Page title and header mention to-do lists
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element_by_tag_name("h1").text

        self.assertIn("To-Do", header_text)

        # User is invited to add a to-do item immediately
        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        # User inputs to-do "By some stuff"
        inputbox.send_keys("Buy some stuff")
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # Check if items are displayed on the page
        self.wait_for_row_in_list_table("1. Buy some stuff")

        # Add a second item "Buy some other stuff"
        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        inputbox.send_keys("Buy some other stuff")
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.wait_for_row_in_list_table("2. Buy some other stuff")
