# Generated by Django 4.2.5 on 2023-10-21 07:59

import catalog.validators
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
                    "normilized_name",
                    models.CharField(
                        auto_created=True,
                        max_length=150,
                        verbose_name="Нормализоваванное имя",
                    ),
                ),
                (
                    "id",
                    models.BigAutoField(
                        primary_key=True, serialize=False, verbose_name="id"
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True, verbose_name="опубликовано"
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Максимум 150 символов",
                        max_length=150,
                        unique=True,
                        verbose_name="название",
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
                        verbose_name="слаг",
                    ),
                ),
                (
                    "weight",
                    models.IntegerField(
                        default=100,
                        validators=[
                            django.core.validators.MaxValueValidator(32767),
                            django.core.validators.MinValueValidator(1),
                        ],
                        verbose_name="вес",
                    ),
                ),
            ],
            options={
                "verbose_name": "категория",
                "verbose_name_plural": "категории",
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "normilized_name",
                    models.CharField(
                        auto_created=True,
                        max_length=150,
                        verbose_name="Нормализоваванное имя",
                    ),
                ),
                (
                    "id",
                    models.BigAutoField(
                        primary_key=True, serialize=False, verbose_name="id"
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True, verbose_name="опубликовано"
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Максимум 150 символов",
                        max_length=150,
                        unique=True,
                        verbose_name="название",
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
                        verbose_name="слаг",
                    ),
                ),
            ],
            options={
                "verbose_name": "тег",
                "verbose_name_plural": "теги",
            },
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "normilized_name",
                    models.CharField(
                        auto_created=True,
                        max_length=150,
                        verbose_name="Нормализоваванное имя",
                    ),
                ),
                (
                    "id",
                    models.BigAutoField(
                        primary_key=True, serialize=False, verbose_name="id"
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True, verbose_name="опубликовано"
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Максимум 150 символов",
                        max_length=150,
                        unique=True,
                        verbose_name="название",
                    ),
                ),
                (
                    "text",
                    models.TextField(
                        help_text="Должно содержать по крайней мере одно слово 'Превосходно' или 'Роскошно'",
                        validators=[
                            catalog.validators.ValidateMustContain(
                                "превосходно", "роскошно"
                            )
                        ],
                        verbose_name="текст",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        help_text="Выберите категорию",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="item_category",
                        to="catalog.category",
                        verbose_name="категория",
                    ),
                ),
                (
                    "tags",
                    models.ManyToManyField(
                        to="catalog.tag", verbose_name="теги"
                    ),
                ),
            ],
            options={
                "verbose_name": "товар",
                "verbose_name_plural": "товары",
            },
        ),
    ]
