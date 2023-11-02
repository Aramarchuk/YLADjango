import django.core
from django.db import models
from django.utils.safestring import mark_safe
from sorl.thumbnail import get_thumbnail

from catalog.validators import ValidateMustContain
from core.models import CatalogAbstraction


def item_directory_path(instance, filename):
    return (
        f"catalog/{str(instance.item.id)[:3].zfill(3)}"
        f"/{str(instance.item.id)}/{filename}"
    )


class Tag(CatalogAbstraction):
    slug = models.TextField(
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
    slug = models.TextField(
        unique=True,
        verbose_name=("слаг"),
        validators=[
            django.core.validators.MaxLengthValidator(200),
            django.core.validators.RegexValidator(regex=r"[-a-zA-Z\d_]+"),
        ],
    )
    weight = models.IntegerField(
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
    text = models.TextField(
        verbose_name=("текст"),
        help_text=(
            "Должно содержать по крайней мере одно слово "
            "'Превосходно' или 'Роскошно'"
        ),
        validators=[ValidateMustContain("превосходно", "роскошно")],
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name=("теги"),
        default=None,
    )
    category = models.ForeignKey(
        "category",
        on_delete=models.CASCADE,
        related_name="item_category",
        help_text="Выберите категорию",
        verbose_name=("категория"),
    )

    def image_tmb(self):
        if self.main_image.image:
            return mark_safe(
                f"<img src='{self.main_image.get_image_50x50.url}'>"
            )
        return "Нет изображения"

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    image_tmb.short_description = "превью"
    image_tmb.allow_tags = True


class ImageBaseModel(models.Model):
    image = models.ImageField(
        "image",
        upload_to=item_directory_path,
        default=None,
    )

    @property
    def get_image_300x300(self):
        return get_thumbnail(
            self.image,
            "300x300",
            crop="center",
            quality=51,
        )

    @property
    def get_image_50x50(self):
        return get_thumbnail(
            self.image,
            "50x50",
            crop="center",
            quality=51,
        )

    def __str__(self):
        return self.item.name

    class Meta:
        abstract = True


class MainImage(ImageBaseModel):
    item = models.OneToOneField(
        "Item",
        verbose_name=("Главное изображение"),
        on_delete=models.CASCADE,
        related_name="main_image",
    )

    list_display = "image_tmb"

    class Meta:
        verbose_name = "главное изображение"
        verbose_name_plural = "главные изображения"


class Image(ImageBaseModel):
    item = models.ForeignKey(
        "Item",
        verbose_name=("item"),
        on_delete=models.CASCADE,
        related_name="images",
    )

    class Meta:
        verbose_name = "фото"
        verbose_name_plural = "фото"
