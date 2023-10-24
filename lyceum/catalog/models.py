import django.core
import django.db

from lyceum.catalog.validators import ValidateMustContain
from lyceum.core.models import CatalogAbstraction


class Tag(CatalogAbstraction):
    slug = django.db.models.TextField(
        unique=True,
        verbose_name=("слаг"),
        validators=[
            django.core.validators.MaxLengthValidator(200),
            django.core.validators.RegexValidator(regex=r"[-a-zA-Z\d_]+"),
        ],
    )

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"


class Category(CatalogAbstraction):
    slug = django.db.models.TextField(
        unique=True,
        verbose_name=("слаг"),
        validators=[
            django.core.validators.MaxLengthValidator(200),
            django.core.validators.RegexValidator(regex=r"[-a-zA-Z\d_]+"),
        ],
    )
    weight = django.db.models.IntegerField(
        default=100,
        validators=[
            django.core.validators.MaxValueValidator(32767),
            django.core.validators.MinValueValidator(1),
        ],
        verbose_name=("вес"),
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Item(CatalogAbstraction):
    text = django.db.models.TextField(
        verbose_name=("текст"),
        help_text=(
            "Должно содержать по крайней мере одно слово "
            "'Превосходно' или 'Роскошно'"
        ),
        validators=[ValidateMustContain("превосходно", "роскошно")],
    )
    tags = django.db.models.ManyToManyField(Tag, verbose_name=("теги"))
    category = django.db.models.ForeignKey(
        "category",
        on_delete=django.db.models.CASCADE,
        related_name="item_category",
        help_text="Выберите категорию",
        verbose_name=("категория"),
    )

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"
