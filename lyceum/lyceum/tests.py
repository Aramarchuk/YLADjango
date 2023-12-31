from unittest.mock import MagicMock

from django.test import Client, override_settings, TestCase
from parameterized import parameterized

from lyceum.middleware import SimpleMiddleware


__all__ = ()


class StaticUrlTests(TestCase):
    @parameterized.expand(
        [
            ("Я чайник", "Я кинйач"),
            ("zzzРаз0tre", "zzzРаз0tre"),
            ("Привет, мир!", "тевирП, рим!"),
            ("Hello, world!", "Hello, world!"),
        ],
    )
    @override_settings(ALLOW_REVERSE=True)
    def test_positive_middleware(self, text, excepted):
        get_response = MagicMock()
        get_response.return_value.content = text.encode()
        request = Client().get("/")

        middleware = SimpleMiddleware(get_response)
        responses = tuple(middleware(request).content for _ in range(10))

        self.assertIn(excepted, responses)

    @parameterized.expand(
        [
            ("Я чайник", "Я кинйач"),
            ("Привет, мир!", "тевирП, рим!"),
        ],
    )
    @override_settings(ALLOW_REVERSE=False)
    def test_negative_allowe_middleware(self, text, excepted):
        get_response = MagicMock()
        get_response.return_value.content = text.encode()
        request = Client().get("/")

        middleware = SimpleMiddleware(get_response)
        responses = tuple(middleware(request).content for _ in range(10))

        self.assertNotIn(excepted, responses)
