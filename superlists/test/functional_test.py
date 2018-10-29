import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox(executable_path="/usr/local/bin/geckodriver")

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrive_it_later(self):
        # Browser opens the main page
        self.browser.get("http://localhost:8000")

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

        # Add a second item "Buy some other stuff"
        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        inputbox.send_keys("Buy some other stuff")
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # Check if items are displayed on the page
        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertIn(
            "1. Buy some stuff",
            [row.text for row in rows],
            f"First to-do item did not appear in the table. Contents were: \n{table.text}",
        )
        self.assertIn(
            "2. Buy some other stuff",
            [row.text for row in rows],
            f"2nd to-do item did not appear in the table. Contents were: \n{table.text}",
        )


if __name__ == "__main__":
    unittest.main(warnings="ignore")
