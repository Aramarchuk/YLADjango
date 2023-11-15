from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from users.models import Profile

__all__ = ()


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text="Required")

    class Meta:
        model = User
        fields = (
            User.username.field.name,
            User.email.field.name,
            "password1",
            "password2",
        )

    def clean(self):
        cleaned_data = super().clean()
        email = self.cleaned_data["email"].lower().strip()
        left_part = email.split("@")[0].replace("+", "")
        right_part = email.split("@")[1].replace("ya.ru", "yandex.ru")
        if right_part == "gmail.com":
            left_part = left_part.replace(".", "")
        elif right_part == "yandex.ru":
            left_part = left_part.replace(".", "-")
        cleaned_data["email"] = left_part + "@" + right_part
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This mail already registered")
        return cleaned_data


class UserChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = User
        fields = ("username", "email")


class ProfileChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
        self.fields["image"].widget.attrs["type"] = "file"
        self.fields["coffee_count"].widget.attrs["readonly"] = True

    class Meta:
        model = Profile
        fields = (
            Profile.birthday.field.name,
            Profile.image.field.name,
            Profile.coffee_count.field.name,
        )
