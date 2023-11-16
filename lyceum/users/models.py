import sys

from django.contrib.auth.models import (
    User as BaseUser,
    UserManager as BaseUserManager,
)
from django.db import models


__all__ = "Profile"


class UserManager(BaseUserManager):
    def active(self):
        return (
            self.get_queryset()
            .filter(is_active=True)
            .select_related(
                "profile",
            )
        )

    def by_mail(self, email):
        return self.active().get(email=email)


class User(BaseUser):
    objects = UserManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "migrate" not in sys.argv and "makemigrations" not in sys.argv:
            BaseUser._meta.get_field("email")._unique = True

    class Meta(BaseUser.Meta):
        proxy = True


class Profile(models.Model):
    def upload_path(self, filename):
        return f"image/{str(self.id)}"

    user = models.OneToOneField(
        BaseUser,
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
