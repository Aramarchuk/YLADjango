from http import HTTPStatus

import django.core
from django.test import Client, TestCase
from parameterized import parameterized

from catalog import models


__all__ = ("StaticUrlTests", "StaticModelTests")


class StaticUrlTests(TestCase):
    @parameterized.expand(
        [
            ("/text", HTTPStatus.NOT_FOUND),
            ("/o", HTTPStatus.NOT_FOUND),
            ("/re/12r34", HTTPStatus.NOT_FOUND),
            ("/re/0", HTTPStatus.NOT_FOUND),
            ("/re/-1", HTTPStatus.NOT_FOUND),
            ("/converter/12r34", HTTPStatus.NOT_FOUND),
            ("/converter/0", HTTPStatus.NOT_FOUND),
            ("/converter/-1", HTTPStatus.NOT_FOUND),
        ],
    )
    def test_catalog_negative_endpoint(self, item, excepted):
        response = Client().get(f"/catalog{item}/")
        self.assertEqual(response.status_code, excepted)


class StaticModelTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = models.Category.objects.create(
            is_published=True,
            name="Тестовая категория",
            slug="test-category-slug",
            weight=100,
        )
        cls.tag = models.Tag.objects.create(
            is_published=True,
            name="Тестовый тег",
            slug="test-tag-slug",
        )

    @parameterized.expand(
        [
            ("Without", "Not Prevoshodno"),
            ("Empty", ""),
            ("Splitted", "П р е в о с х о д н о"),
        ],
    )
    def test_create_perfection_validators_negative(self, names, texts):
        item_count = models.Item.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.item = models.Item(
                name=names,
                text=texts,
                category=StaticModelTests.category,
            )
            self.item.full_clean()
            self.item.save()
            self.item.tags.add(StaticModelTests.tag)
            self.item.tags.save()
        self.assertEqual(models.Item.objects.count(), item_count)

    @parameterized.expand(
        [
            ("test-name", "Превосходно"),
            ("0", "Восхитительно и Превосходно"),
            ("0", "Не только превосходно"),
            ("0", "ПреПре?Превосходно"),
        ],
    )
    def test_create_item_positive(self, names, texts):
        item_count = models.Item.objects.count()
        self.item = models.Item(
            name=names,
            text=texts,
            category=StaticModelTests.category,
        )
        self.item.full_clean()
        self.item.save()
        self.item.tags.add(StaticModelTests.tag)
        self.assertEqual(models.Item.objects.count(), item_count + 1)


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
