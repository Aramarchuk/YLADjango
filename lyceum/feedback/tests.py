from pathlib import Path

import django
from django.test import Client, override_settings, TestCase
from feedback.forms import AuthorForm, FeedbackForm
from feedback.models import Feedback, FeedbackFile

__all__ = "FormTest"


class FormTest(TestCase):
    def test_feedback_context(self):
        response = Client().get(django.urls.reverse("feedback:feedback"))
        self.assertIn("form", response.context)

    def test_feedback_context_type(self):
        response = Client().get(django.urls.reverse("feedback:feedback"))
        self.assertIsInstance(response.context["feedback_form"], FeedbackForm)

    def test_feedback_context_label_and_help(self):
        response = Client().get(django.urls.reverse("feedback:feedback"))
        test_form = response.context["feedback_form"]
        test_author_form = response.context["author_form"]
        self.assertEqual(test_form.fields["text"].label, "Текст")
        self.assertEqual(test_author_form.fields["mail"].label, "Почта")
        self.assertEqual(
            test_author_form.fields["mail"].help_text,
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
            "mail": "examplegmail.com",
            "name": "Example Name",
        }
        form = AuthorForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Введите правильный адрес электронной почты.",
            form.errors["mail"],
        )

    def test_feedback_empty(self):
        author_data = {
            "mail": "",
            "name": "",
        }
        fb_data = {
            "text": "",
        }
        author_form = AuthorForm(author_data)
        fb_form = FeedbackForm(fb_data)
        self.assertFalse(author_form.is_valid())
        self.assertFalse(fb_form.is_valid())
        self.assertTrue(author_form.has_error("mail"))

    def test_count_feedback(self):
        old_len = Feedback.objects.all().count()
        author_data = {
            "mail": "example@gmail.com",
            "name": "q",
        }
        fb_data = {
            "text": "t",
        }
        author_form = AuthorForm(author_data)
        fb_form = FeedbackForm(fb_data)
        self.assertTrue(author_form.is_valid())
        author_form.save()
        fb = fb_form.save(commit=False)
        author = author_form.save(commit=False)
        fb.author = author
        fb.save()
        author.save()
        self.assertEqual(Feedback.objects.all().count(), old_len + 1)

    def test_valid_form_db(self):
        old_len = Feedback.objects.all().count()
        data = {
            "text": "Тестовый Текст",
            "mail": "example@gmail.com",
            "name": "Example Name",
        }
        self.client.post("/feedback/", data=data)
        self.assertEqual(Feedback.objects.all().count(), old_len + 1)

    @override_settings(
        MEDAI_ROOT=django.conf.settings.BASE_DIR / "feedback/test_files/",
    )
    def test_valid_file_form(self):
        print(django.conf.settings.BASE_DIR)
        old_len = FeedbackFile.objects.all().count()
        file = Path("feedback/test_files/test_file.txt").open()
        data = {
            "text": "Тестовый Текст",
            "mail": "example@gmail.com",
            "name": "Example Name",
            "files": [file],
        }
        self.client.post("/feedback/", data=data)
        self.assertEqual(FeedbackFile.objects.all().count(), old_len + 1)
