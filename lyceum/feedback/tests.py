import django
from django.test import Client, TestCase

from feedback.forms import FeedbackForm

__all__ = "FormTest"


class FormTest(TestCase):
    def test_feedback_context(self):
        response = Client().get(django.urls.reverse("feedback:feedback"))
        self.assertIn("form", response.context)

    def test_feedback_context_type(self):
        response = Client().get(django.urls.reverse("feedback:feedback"))
        self.assertIsInstance(response.context["form"], FeedbackForm)

    def test_feedback_context_label_and_help(self):
        response = Client().get(django.urls.reverse("feedback:feedback"))
        test_form = response.context["form"]
        self.assertEqual(test_form.fields["text"].label, "Текст")
        self.assertEqual(test_form.fields["mail"].label, "Почта")
        self.assertEqual(
            test_form.fields["mail"].help_text,
            "Введите вашу почту",
        )

        self.assertIn("form", response.context)

    def test_feedback_redirect(self):
        form_data = {
            "text": "testText",
            "mail": "example@gmail.com",
        }
        response = Client().post(
            django.urls.reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )

        self.assertRedirects(
            response,
            django.urls.reverse("feedback:feedback"),
        )
