from django.contrib.auth.models import User
from django.db import models


__all__ = "Profile"


class Profile(models.Model):
    def upload_path(self, filename):
        return f"image/{str(self.id)}"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="profile",
    )
    birthday = models.DateField(
        verbose_name="дата рождения",
        blank=True,
        null=True,
    )
    image = models.ImageField(
        verbose_name=("аватарка"),
        upload_to=upload_path,
        blank=True,
        null=True,
    )
    coffee_count = models.PositiveIntegerField(
        verbose_name="выпито кофе",
        default=0,
    )
