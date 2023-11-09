from django.conf import settings
from django.db import models


__all__ = ()


CHOISES = [
    ("IN", "в обработке"),
    ("GET", "получено"),
    ("ANS", "ответ дан"),
]


class Feedback(models.Model):
    class Meta:
        verbose_name = "Фидбек"
        verbose_name_plural = "Фидбеки"

    text = models.fields.TextField(
        verbose_name="текстовое поле",
    )
    created_on = models.fields.DateTimeField(
        auto_now_add=True,
        verbose_name=("дата и время создания"),
    )
    mail = models.EmailField(
        verbose_name=("почта"),
        max_length=254,
    )
    name = models.fields.TextField(
        verbose_name="имя",
        null=True,
        blank=True,
    )
    status = models.fields.TextField(
        verbose_name="статус обработки",
        choices=CHOISES,
        default="GET",
    )


class StatusLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    timestamp = models.DateTimeField(
        ("время"),
        auto_now_add=True,
    )
    from_status = models.fields.TextField(
        verbose_name="старый статус обработки",
        choices=CHOISES,
        db_column="from",
    )
    to_status = models.fields.TextField(
        verbose_name="новый статус обработки",
        choices=CHOISES,
        db_column="to",
    )

    class Meta:
        verbose_name = "Лог изменения"
        verbose_name_plural = "Лог изменений"
