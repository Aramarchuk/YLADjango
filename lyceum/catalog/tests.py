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
    fixtures = ["fixtures/data1.json"]

    def test_catalog_context_positive(self):
        response = Client().get(django.urls.reverse("catalog:item_list"))
        self.assertIn("items", response.context)

    def test_catalog_items_size(self):
        response = Client().get(django.urls.reverse("catalog:item_list"))
        self.assertEqual(len(response.context["items"]), 3)

    def test_item_type(self):
        response = Client().get(
            django.urls.reverse("catalog:item_detail", args=[1]),
        )
        self.assertIsInstance(response.context["item"], models.Item)

    def test_catalog_context_detail(self):
        response = Client().get(
            django.urls.reverse("catalog:item_detail", args=[1]),
        )
        self.assertIn("item", response.context)

    def test_catalog_items_types(self):
        response = Client().get(django.urls.reverse("catalog:item_list"))
        self.assertTrue(
            all(
                isinstance(
                    item,
                    models.Item,
                )
                for item in response.context["items"]
            ),
        )


class CheckSQLOptinization(TestCase):
    fixtures = ["fixtures/data1.json"]

    def check_content_value(
        self,
        item,
        exists,
        prefetched,
        not_loaded,
    ):
        check_dict = item.__dict__

        for value in exists:
            self.assertIn(value, check_dict)

        for value in prefetched:
            self.assertIn(value, check_dict["_prefetched_objects_cache"])

        for value in not_loaded:
            self.assertNotIn(value, check_dict)

    def test_loaded_value_list(self):
        response = Client().get(django.urls.reverse("catalog:item_list"))
        for item in response.context["items"]:
            self.check_content_value(
                item,
                (
                    "name",
                    "text",
                    "category_id",
                ),
                ("tags",),
                (
                    "is_on_main",
                    "main_image",
                    "images",
                    "is_published",
                ),
            )

    def test_loaded_value_detail(self):
        response = Client().get(
            django.urls.reverse("catalog:item_detail", args=[1]),
        )
        item = response.context["item"]
        self.check_content_value(
            item,
            (
                "name",
                "text",
                "category_id",
            ),
            ("tags",),
            (
                "is_on_main",
                "main_image",
                "images",
                "is_published",
            ),
        )
        self.check_content_value(
            item.tags.all()[0],
            ("name",),
            (),
            ("is_published",),
        )
