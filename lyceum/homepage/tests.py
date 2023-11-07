from http import HTTPStatus

from django.test import Client, override_settings, TestCase
import django.urls

from catalog import models


__all__ = ()


class StaticUrlTests(TestCase):
    def test_homepage_positive_endpoint(self):
        response = Client().get("/")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_coffee_httpstatus_endpoint(self):
        response = Client().get("/coffee/")
        self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)

    @override_settings(ALLOW_REVERSE=False)
    def test_coffee_text_endpoint(self):
        response = Client().get("/coffee/")
        self.assertEqual(
            response.content,
            "Я чайник".encode(),
        )


class ContextTests(TestCase):
    fixtures = ["fixtures/data1.json"]

    def test_home_context_positive(self):
        response = Client().get(django.urls.reverse("homepage:home"))
        self.assertIn("items", response.context)

    def test_home_context_count(self):
        response = Client().get(django.urls.reverse("homepage:home"))
        self.assertEqual(response.context["items"].count(), 1)

    def test_home_types_context(self):
        response = Client().get(django.urls.reverse("homepage:home"))
        self.assertTrue(
            all(
                isinstance(
                    item,
                    models.Item,
                )
                for item in response.context["items"]
            ),
        )
