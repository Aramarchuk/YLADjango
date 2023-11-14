from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from users.models import Profile

__all__ = ()


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text="Required")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


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
        self.fields["avatar"].widget.attrs["type"] = "file"

    class Meta:
        model = Profile
        fields = ("birthday", "avatar")
