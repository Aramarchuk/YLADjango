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
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.published_category = models.Category.objects.create(
            is_published=True,
            name="Test Public Cat",
            slug="tpc",
        )
        cls.unpublished_category = models.Category.objects.create(
            is_published=False,
            name="Test not Public Cat",
            slug="tnpc",
        )

        cls.published_tag = models.Tag.objects.create(
            is_published=True,
            name="Test Public Tag",
            slug="tpt",
        )
        cls.unpublished_tag = models.Tag.objects.create(
            is_published=False,
            name="Test not Public Tag",
            slug="tnpt",
        )

        cls.published_item = models.Item.objects.create(
            is_published=True,
            is_on_main=True,
            category=cls.unpublished_category,
            name="item public test",
            text="Превосходно",
        )
        cls.unpublished_item = models.Item.objects.create(
            is_published=False,
            is_on_main=True,
            category=cls.published_category,
            name="item not public test",
            text="Превосходно",
        )

        cls.unpublished_category.save()
        cls.published_category.save()
        cls.published_tag.save()
        cls.published_tag.save()
        cls.published_item.save()
        cls.unpublished_item.save()

        cls.unpublished_item.tags.add(cls.published_tag)
        cls.published_item.tags.add(cls.unpublished_tag)

    def test_home_context_positive(self):
        response = Client().get(django.urls.reverse("homepage:home"))
        self.assertIn("items", response.context)

    def test_home_context_count(self):
        response = Client().get(django.urls.reverse("homepage:home"))
        self.assertEqual(response.context["items"].count(), 1)
