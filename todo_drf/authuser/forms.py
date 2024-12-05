from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from .models import User

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django.contrib.auth import authenticate

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
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(
        attrs={'type': "password",
               'class': "form-control",
               'placeholder': "Повторите пароль",
               }
    ))

    class Meta:
        model = get_user_model()
        fields = ["email", "name", "password1", "password2"]

class ChangeUsernameForm(forms.ModelForm):
    name = forms.CharField(label='Ваше имя', validators=[only_letters], widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'type': "name",
            'placeholder': "Введите имя",
        }
    ))

    class Meta:
        model = User
        fields = ['name', ]

class CustomPasswordChangeForm(forms.Form):
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput(attrs={'type': "password",
                                                                                            'class': "form-control",
                                                                                            'placeholder': "Старый пароль", })
                                   )
    new_password1 = forms.CharField(label='Новый пароль',
                                    widget=forms.PasswordInput(attrs={'type': "password",
                                                                      'class': "form-control",
                                                                      'placeholder': "Новый пароль", })
                                    )
    new_password2 = forms.CharField(label='Повторите новый пароль',
                                    widget=forms.PasswordInput(attrs={'type': "password",
                                                                      'class': "form-control",
                                                                      'placeholder': "Повторите новый пароль", }))
    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get("old_password")
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")
        user = self.user

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("Пароли не совпадают.")
        if old_password:
            if not authenticate(email=user.email, password=old_password):
                raise forms.ValidationError("Неверный текущий пароль")
            if old_password == new_password1:
                raise forms.ValidationError("Новый пароль не может быть такой же как и старый")
        return cleaned_data

    def save(self, user):
        user.set_password(self.cleaned_data['new_password1'])
        user.save()