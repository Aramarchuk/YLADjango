from http import HTTPStatus

from django.test import Client, override_settings, TestCase


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
