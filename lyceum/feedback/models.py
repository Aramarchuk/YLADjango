from django.db import models


__all__ = ()


class Feedback(models.Model):
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


# Create your models here.
