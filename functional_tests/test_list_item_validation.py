from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def get_error_element(self):
        return self.browser.find_element_by_css_selector(".text-danger")

    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)
        # The home page refreshes, and there is an error message saying
        # that list items cannot be blank
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector("#id_text:invalid")
        )
        # She tries again with some text for the item, which now works
        self.get_item_input_box().send_keys("Buy milk")
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector("#id_text:valid")
        )
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1. Buy milk")
        # Perversely, she now decides to submit a second blank list item
        self.get_item_input_box().send_keys(Keys.ENTER)

        # And she can correct it by filling some text in
        self.get_item_input_box().send_keys("Make tea")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1. Buy milk")
        self.wait_for_row_in_list_table("2. Make tea")

    def test_cannot_add_duplicate_items(self):
        # Edith goes to the home page and starts a new list
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys("Buy wellies")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1. Buy wellies")

        # She accidentally tries to enter a duplicate item
        self.get_item_input_box().send_keys("Buy wellies")
        self.get_item_input_box().send_keys(Keys.ENTER)

        # She sees a helpful error message
        self.wait_for(
            lambda: self.assertEqual(
                self.get_error_element().text, "You've already got this in your list"
            )
        )

    def test_error_message_are_cleare_on_inpt(self):
        # First test duplicate item error cleared
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys("Banter too thick")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1. Banter too thick")
        self.get_item_input_box().send_keys("Banter too thick")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertTrue(self.get_error_element().is_displayed()))
        self.get_item_input_box().send_keys("a")
        self.wait_for(lambda: self.assertFalse(self.get_error_element().is_displayed()))
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Second test empty input error cleared
        self.get_item_input_box().send_keys(" ")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertTrue(self.get_error_element().is_displayed()))
        self.get_item_input_box().send_keys("L")
        self.wait_for(lambda: self.assertFalse(self.get_error_element().is_displayed()))
