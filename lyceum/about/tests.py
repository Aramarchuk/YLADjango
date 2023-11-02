from django.test import Client, TestCase
import django.urls


__all__ = ("StaticUrlTests", )


class StaticUrlTests(TestCase):
    def test_about_endpoint(self):
        response = Client().get(django.urls.reverse("about:about"))
        self.assertEqual(response.status_code, 200)
