from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest


class LayoutsAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        inputbox = self.get_item_input_box()

        def assert_inputbox_centered(browser):
            inputbox = self.get_item_input_box()
            self.assertAlmostEqual(
                inputbox.location["x"] + inputbox.size["width"] / 2, 512, delta=10
            )

        assert_inputbox_centered(self.browser)

        inputbox.send_keys("testing")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1. testing")
        assert_inputbox_centered(self.browser)
