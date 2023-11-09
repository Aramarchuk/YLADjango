from django.contrib.auth.models import User
from django.db import models


__all__ = ()


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
        default=None,
    )
    status = models.fields.TextField(
        verbose_name="статус обработки",
        choices=[
            ("IN", "в обработке"),
            ("GET", "получено"),
            ("ANS", "ответ дан"),
        ],
        default="GET",
    )


class StatusLog(models.Model):
    class Meta:
        verbose_name = "Лог изменения"
        verbose_name_plural = "Лог изменений"

    user = models.ForeignKey(
        User,
        verbose_name=("пользователь"),
        on_delete=models.CASCADE,
    )
    timestamp = models.DateTimeField(
        ("время"),
        auto_now_add=True,
    )
    from_status = models.fields.TextField(
        verbose_name="статус обработки",
        choices=[
            ("IN", "в обработке"),
            ("GET", "в обработке"),
            ("ANS", "ответ дан"),
        ],
    )
    to = models.fields.TextField(
        verbose_name="статус обработки",
        choices=[
            ("IN", "в обработке"),
            ("GET", "в обработке"),
            ("ANS", "ответ дан"),
        ],
    )
