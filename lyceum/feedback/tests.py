import django
from django.test import Client, TestCase


from feedback.forms import FeedbackForm
from feedback.models import Feedback

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
            "name": "Example Name",
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

    def test_feedback_valid_form(self):
        data = {
            "text": "Тестовый Текст",
            "mail": "example@gmail.com",
            "name": "Example Name",
        }

        self.assertTrue(FeedbackForm(data).is_valid())

    def test_feedback_invalid_email(self):
        data = {
            "text": "Тестовый Текст",
            "mail": "examplegmail.com",
            "name": "Example Name",
        }
        form = FeedbackForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Введите правильный адрес электронной почты.",
            form.errors["mail"],
        )

    def test_feedback_empty(self):
        data = {
            "text": "",
            "mail": "",
        }
        form = FeedbackForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error("mail"))

    def test_count_feedback(self):
        old_len = len(Feedback.objects.all())
        data = {
            "text": "Тестовый Текст",
            "mail": "example@gmail.com",
            "name": "Example Name",
        }
        form = FeedbackForm(data=data)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(len(Feedback.objects.all()), old_len + 1)
