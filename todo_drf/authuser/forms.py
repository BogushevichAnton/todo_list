from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class AuthForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(
        attrs={'class': 'form-control',
               'type': "email",
               'placeholder': "Введите email",
               }
    ))

    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'type': "password",
               'class': "form-control",
               'placeholder': "Введите пароль",

               }
    ))

    class Meta:
        model = get_user_model()


class RegisterForm(UserCreationForm):
    name = forms.CharField(label='Ваше имя', widget=forms.TextInput(
        attrs={'class': 'form-input'}
    ))

    class Meta:
        model = get_user_model()
        fields = ["email", "name", "password1", "password2"]
