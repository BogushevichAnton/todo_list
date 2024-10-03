from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def only_letters(value: str):
    if not value.isalpha():
        raise ValidationError(_('Введите только буквы'))

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
    email = forms.CharField(label='Логин', widget=forms.TextInput(
        attrs={'class': 'form-control',
               'type': "email",
               'placeholder': "Введите email",
               }
    ))

    name = forms.CharField(label='Ваше имя', validators=[only_letters], widget=forms.TextInput(
        attrs={
               'class': 'form-control',
               'type': "name",
               'placeholder': "Введите имя",
               }
    ))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'type': "password",
               'class': "form-control",
               'placeholder': "Введите пароль",
               }
    ))
    password2 = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'type': "password",
               'class': "form-control",
               'placeholder': "Введите пароль",

               }
    ))

    class Meta:
        model = get_user_model()
        fields = [ "email", "name", "password1", "password2"]
