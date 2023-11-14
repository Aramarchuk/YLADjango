from django.contrib.auth.models import User
from django.db import models


__all__ = "Profile"


class Profile(models.Model):
    def upload_path(self):
        return f"avatar/{str(self.id)}"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    birthday = models.DateField(
        verbose_name="дата рождения",
        blank=True,
        null=True,
    )
    avatar = models.ImageField(
        ("аватарка"),
        upload_to=upload_path,
    )
    coffee_count = models.IntegerField(
        verbose_name="выпито кофе",
        default=0,
    )
