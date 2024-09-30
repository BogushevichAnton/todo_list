from django import forms

from authuser.models import User


class AuthForm(forms.Form):
    email = forms.EmailField(label='email', max_length=255)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
