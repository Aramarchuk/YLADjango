from django.test import override_settings, TestCase

import users.forms
import users.models

__all__ = "FormTest"


class ActivationTests(TestCase):
    @override_settings(DEFAULT_USER_IS_ACTIVE=True)
    def default_activation_true_test(self):
        old_len = users.models.User.objects.all().count()
        data = {
            "username": "New username",
            "mail": "example@gmail.com",
            "password1": "Example0password",
            "password2": "Example0password",
        }

        self.assertTrue(users.forms.SignupForm(data).is_valid())
        self.client.post("/auth/signup", data=data)
        self.assertEqual(users.models.User.objects.all().count(), old_len + 1)
        self.assertTrue(
            users.models.User.objects.get(
                username=data["username"],
            ).is_active,
        )

    @override_settings(DEFAULT_USER_IS_ACTIVE=False)
    def default_activation_false_test(self):
        old_len = users.models.User.objects.all().count()
        data = {
            "username": "New username",
            "mail": "example@gmail.com",
            "password1": "Example0password",
            "password2": "Example0password",
        }

        self.assertTrue(users.forms.SignupForm(data).is_valid())
        self.client.post("/auth/signup", data=data)
        self.assertEqual(users.models.User.objects.all().count(), old_len + 1)
        self.assertFalse(
            users.models.User.objects.get(
                username=data["username"],
            ).is_active,
        )
