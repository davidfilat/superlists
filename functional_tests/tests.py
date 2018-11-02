import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

MAX_WAIT = 10
GECKODRIVER = "/usr/local/bin/geckodriver"


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
        self.browser = webdriver.Firefox(executable_path=GECKODRIVER)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_for_one_user(self):
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

        # Add a second item "Buy some other stuff"
        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        inputbox.send_keys("Buy some other stuff")
        inputbox.send_keys(Keys.ENTER)
        # Check if items are displayed on the page

        self.wait_for_row_in_list_table("2. Buy some other stuff")
        self.wait_for_row_in_list_table("1. Buy some stuff")

    def test_multiple_users_can_start_lists_at_different_urls(self):
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, "/lists/.+")
        # Now a new user, Francis, comes along to the site.

        ## We use a new browser session to make sure that no information
        ## of Edith's is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox(executable_path=GECKODRIVER)
        # Francis visits the home page.  There is no sign of Edith's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("Buy some stuff", page_text)
        self.assertNotIn("some other stuff", page_text)

        # Francis starts a new list by entering a new item. He is less interesting than Edith...
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("Buy milk")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1. Buy milk")

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "/lists/.+")
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("Buy some stuff", page_text)
        self.assertIn("Buy milk", page_text)

        # Satisfied, they both go back to sleep
