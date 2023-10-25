import django.core
import django.db
from django.utils.safestring import mark_safe
from sorl.thumbnail import get_thumbnail

from catalog.validators import ValidateMustContain
from core.models import CatalogAbstraction


class Image(django.db.model.Model):
    image = django.db.models.models.ImageField(
        ("Изображение"),
        upload_to="catalog/",
        height_field=300,
        width_field=300,
        max_length=None
    )

    def get_image_300x300(self):
        return get_thumbnail(self.image, "300", quality=51)

    def image_tmb(self):
        if self.image:
            return mark_safe(
                f"<img src='{self.image.url}' width=50>"
            )
        return "Нет изображения"

    list_display = (
        "image_tmb"
    )


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
    main_image = django.db.models.ForeignKey(
        "images",
        on_delete=django.db.models.CASCADE,
        related_name="item_main_image",
        help_text="Загрузите изображение",
        verbose_name=("главное изображение"),
    )
    images = django.db.models.ManyToManyField(
        Image,
        verbose_name=("изображения")
    )
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
