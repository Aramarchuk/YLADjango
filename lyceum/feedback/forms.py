from django import forms
from django.core import validators

from feedback.models import Author, Feedback, FeedbackFile


__all__ = ()


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_file_clean(d, initial) for d in data]
        return single_file_clean(data, initial)


class FeedbackFileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["files"] = forms.FileField(
            widget=MultipleFileInput(attrs={"multiple": True}),
        )
        self.fields["files"].required = False
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = FeedbackFile
        exclude = ["feedback", "file"]


class FeedbackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Feedback
        exclude = ["created_on", "status", "author"]

        labels = {
            "text": "Текст",
        }
        widgets = {
            "text": forms.TextInput(),
        }
        validators = {
            "mail": validators.EmailValidator(
                message="Некорректная почта",
                code=1,
            ),
        }


class AuthorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
            field.field.widget.attrs["style"] = "height:30px"

    class Meta:
        model = Author
        exclude = ["feedback"]

        labels = {
            "mail": "Почта",
            "name": "Имя",
        }
        help_texts = {
            "mail": "Введите вашу почту",
        }
        widgets = {
            "mail": forms.EmailInput(),
        }
        validators = {
            "mail": validators.EmailValidator(
                message="Некорректная почта",
                code=1,
            ),
        }
