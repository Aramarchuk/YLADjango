# Generated by Django 4.2.5 on 2023-10-18 18:00

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        primary_key=True, serialize=False, verbose_name="id"
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True, verbose_name="Опубликовано"
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Максимум 150 символов",
                        max_length=150,
                        verbose_name="Название",
                    ),
                ),
                (
                    "slug",
                    models.TextField(
                        unique=True,
                        validators=[
                            django.core.validators.MaxLengthValidator(200),
                            django.core.validators.RegexValidator(
                                regex="[-a-zA-Z\\d_]+"
                            ),
                        ],
                        verbose_name="Слаг",
                    ),
                ),
                (
                    "weight",
                    models.IntegerField(
                        default=100,
                        validators=[
                            django.core.validators.MaxValueValidator(32767),
                            django.core.validators.MinValueValidator(0),
                        ],
                        verbose_name="Вес",
                    ),
                ),
            ],
            options={
                "verbose_name": "Категория",
                "verbose_name_plural": "Категории",
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        primary_key=True, serialize=False, verbose_name="id"
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True, verbose_name="Опубликовано"
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Максимум 150 символов",
                        max_length=150,
                        verbose_name="Название",
                    ),
                ),
                (
                    "slug",
                    models.TextField(
                        unique=True,
                        validators=[
                            django.core.validators.MaxLengthValidator(200),
                            django.core.validators.RegexValidator(
                                regex="[-a-zA-Z\\d_]+"
                            ),
                        ],
                        verbose_name="Слаг",
                    ),
                ),
            ],
            options={
                "verbose_name": "Тег",
                "verbose_name_plural": "Теги",
            },
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        primary_key=True, serialize=False, verbose_name="id"
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True, verbose_name="Опубликовано"
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Максимум 150 символов",
                        max_length=150,
                        verbose_name="Название",
                    ),
                ),
                (
                    "text",
                    models.TextField(
                        help_text="Должно содержать по крайней мере одно слово 'Превосходно' или 'Роскошно'",
                        verbose_name="Текст",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        help_text="Выберите категорию",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="item_category",
                        to="catalog.category",
                    ),
                ),
                ("tags", models.ManyToManyField(to="catalog.tag")),
            ],
            options={
                "verbose_name": "Товар",
                "verbose_name_plural": "Товары",
            },
        ),
    ]
