from django.contrib import contenttypes
from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve

from lists.models import Item
from lists.views import home_page


# Create your tests here.
class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        response = self.client.get("/")
        html = response.content.decode("utf8")

        self.assertTrue(html.startswith("<html>"))
        self.assertIn("<title>To-Do lists</title>", html)
        self.assertTrue(html.strip().endswith("</html>"))
        self.assertTemplateUsed(response, "home.html")

    def test_can_save_a_POST_request(self):
        self.client.post("/", {"item_text": "A new list item"})
        new_item = Item.objects.first()

        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(new_item.text, "A new list item")

    def test_redirects_after_post(self):
        response = self.client.post("/", {"item_text": "A new list item"})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], "/lists/the-only-list-in-the-world/")


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get("/lists/the-only-list-in-the-world/")
        self.assertTemplateUsed(response, "list.html")

    def test_display_all_items(self):
        Item.objects.create(text="itemey 1")
        Item.objects.create(text="itemey 2")
        response = self.client.get("/lists/the-only-list-in-the-world/")

        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")
