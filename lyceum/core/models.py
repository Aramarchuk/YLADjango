import re

from django.core.exceptions import ValidationError
import django.db


def normilize(value):
    letters = {
        "а": "a",
        "е": "e",
        "о": "o",
        "р": "p",
        "с": "c",
        "т": "t",
        "у": "y",
        "х": "x",
        "м": "m",
        "н": "h",
        "в": "b",
        "к": "k",
    }
    value = value.lower()
    value = re.sub(r"[^\w\s]", "", value)
    value = value.replace(" ", "")
    for el in letters.items():
        value = value.replace(el[0], el[1])
    return value


class CatalogAbstraction(django.db.models.Model):
    id = django.db.models.BigAutoField(primary_key=True, verbose_name="id")
    is_published = django.db.models.BooleanField(
        default=True, verbose_name=("опубликовано")
    )
    name = django.db.models.CharField(
        unique=True,
        verbose_name=("название"),
        max_length=150,
        help_text="Максимум 150 символов",
    )
    normilized_name = django.db.models.CharField(
        unique=True,
        auto_created=True,
        verbose_name=("Нормализоваванное имя"),
        max_length=150,
    )

    def save(self, *args, **kwargs):
        self.normilized_name = normilize(self.title())
        super(CatalogAbstraction, self).save(*args, **kwargs)

    def clean(self):
        if self.normilized_name is None:
            raise ValidationError(
                "Название категории уже занято. Попробуйте другое"
                )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name[:15]
