from django import forms


__all__ = ()


class EchoForm(forms.Form):
    text = forms.TextInput()
