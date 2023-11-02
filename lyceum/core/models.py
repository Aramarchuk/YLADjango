import re

from django.core.exceptions import ValidationError
import django.db
import transliterate


__all__ = ()


ONLY_LETTERS_REGEX = re.compile(r"[^\w]")


class CatalogAbstraction(django.db.models.Model):
    is_published = django.db.models.BooleanField(
        default=True, verbose_name=("опубликовано"),
    )
    name = django.db.models.CharField(
        unique=True,
        verbose_name=("название"),
        max_length=150,
        help_text="Максимум 150 символов",
    )
    normilized_name = django.db.models.CharField(
        editable=False,
        unique=True,
        verbose_name=("Нормализоваванное имя"),
        max_length=150,
    )

    def _generate_normilized_name(self):
        try:
            translitereted = transliterate.translit(
                self.name.lower(), reversed=True,
            )
        except transliterate.exceptions.LanguageDetectionError:
            translitereted = self.name.lower()

        return ONLY_LETTERS_REGEX.sub("", translitereted)

    def save(self, *args, **kwargs):
        self.normilized_name = self._generate_normilized_name()
        super(CatalogAbstraction, self).save(*args, **kwargs)

    def clean(self):
        self.normilized_name = self._generate_normilized_name()
        if (
            type(self)
            .objects.filter(normilized_name=self.normilized_name)
            .exclude(id=self.id)
            .count()
            > 0
        ):
            raise ValidationError("Такое название уже существует")

    class Meta:
        abstract = True

    def __str__(self):
        return self.name[:15]
