import os
import re
import time
from datetime import datetime, timedelta

from django.core import mail
from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest
from gmaily import Gmaily

SUBJECT = "Your login link for Superlists"


class LoginTest(FunctionalTest):
    def wait_for_email(self, test_email, subject):
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body

        start = time.time()
        g = Gmaily()
        try:
            g.login(test_email, os.environ["EMAIL_PASSWORD"])
            now = datetime.now()
            msgs = g.inbox().after(datetime.today())
            msgs._criterias.append(f'(SUBJECT "{SUBJECT}")')

            while time.time() - start < 60:

                for msg in reversed(msgs.all()):
                    if (SUBJECT in msg.subject) and (
                        (datetime.utcnow() - msg.date) < timedelta(minutes=2)
                    ):
                        return msg.text
                time.sleep(5)
        finally:
            g.logout()

    def test_can_get_email_link_to_log_in(self):
        if self.staging_server:
            test_email = "filatdav@gmail.com"
        else:
            test_email = "edith@example.com"

        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name("email").send_keys(test_email)
        self.browser.find_element_by_name("email").send_keys(Keys.ENTER)

        self.wait_for(
            lambda: self.assertIn(
                "Check your email", self.browser.find_element_by_tag_name("body").text
            )
        )
        body = self.wait_for_email(test_email, SUBJECT)

        self.assertIn("Use this link to login", body)
        if self.staging_server:
            url_search = re.search(r"https://.+/.+$", body)
        else:
            url_search = re.search(r"http://.+/.+$", body)

        if not url_search:
            self.fail(f"Could not find url in email body:\n{body}")
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)
        self.browser.get(url)
        self.wait_to_be_logged_in(email=test_email)
        self.browser.find_element_by_link_text("Log out").click()

        self.wait_to_be_logged_out(email=test_email)
