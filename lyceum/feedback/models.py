from django.conf import settings
from django.db import models


__all__ = ()


CHOISES = [
    ("IN", "в обработке"),
    ("GET", "получено"),
    ("ANS", "ответ дан"),
]


class Author(models.Model):
    mail = models.EmailField(
        verbose_name=("почта"),
        max_length=254,
    )
    name = models.fields.TextField(
        verbose_name=("имя"),
        null=True,
        blank=True,
    )
    feedback = models.OneToOneField(
        "Feedback",
        verbose_name=("фидбек"),
        on_delete=models.CASCADE,
        related_name="author",
        null=True,
        blank=True,
    )


class FeedbackFile(models.Model):
    def file_directory_path(self, filename):
        return f"uploads/{str(self.feedback.id)}/{filename}"

    feedback = models.ForeignKey(
        "Feedback",
        verbose_name=("фидбек файла"),
        on_delete=models.CASCADE,
        related_name="feedback",
    )
    file = models.FileField(
        "file",
        upload_to=file_directory_path,
        default=None,
    )


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
    from_status = models.fields.CharField(
        verbose_name="старый статус обработки",
        choices=CHOISES,
        db_column="from",
        max_length=4,
    )
    to = models.fields.TextField(
        verbose_name="новый статус обработки",
        choices=CHOISES,
        db_column="to",
        max_length=4,
    )

    class Meta:
        verbose_name = "Лог изменения"
        verbose_name_plural = "Лог изменений"
