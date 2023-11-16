from django.contrib.auth.backends import BaseBackend

from users.models import User

__all__ = "EmailAuthBackend"


class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        email_valid = User.objects.active().filter(email=username).count() == 1
        if email_valid:
            user = User.objects.get(email=username)
            password_valid = user.check_password(password)
            if password_valid:
                return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
