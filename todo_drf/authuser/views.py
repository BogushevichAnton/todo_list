from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.views.generic import CreateView, UpdateView, FormView
from rest_framework.reverse import reverse_lazy
from django.contrib.auth.password_validation import get_password_validators, ValidationError as PasswordValidationError
from django.shortcuts import render, redirect
from .forms import ChangeUsernameForm, CustomPasswordChangeForm

from authuser.forms import AuthForm, RegisterForm

from django.contrib import messages
from .models import User

# Create your views here.
class Auth(LoginView):
    form_class = AuthForm
    template_name = 'authuser/login.html'

    def get_success_url(self):
        return reverse_lazy('index')

@login_required
def logout_view(request):
    logout(request)
    return redirect('index')


class Register(CreateView):
    form_class = RegisterForm
    template_name = "authuser/register.html"

    def get_success_url(self):
        return reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)
        return super().form_valid(form)


def profile(request):
    user = request.user
    context = {'user': user}
    return render(request, 'authuser/profile.html', context)

class ChangeUsernameView(UpdateView):
    model = User
    template_name = 'authuser/change_user_name.html'  # Замените на имя вашего шаблона
    form_class = ChangeUsernameForm
    success_url = reverse_lazy('profile')  # Или любой другой URL, куда перенаправить после успешного изменения

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Имя пользователя успешно изменено!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка при изменении имени пользователя.')
        return super().form_invalid(form)

class PasswordChangeView(FormView):
    template_name = 'authuser/change_user_password.html'
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('profile')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.user = self.request.user
        return form

    def form_valid(self, form):
        try:
            for validator in get_password_validators(settings.AUTH_PASSWORD_VALIDATORS):
                validator.validate(form.cleaned_data['new_password1'])
        except PasswordValidationError as e:
            for message in e.messages: # Перебираем все сообщения об ошибках
                form.add_error('new_password1', message) # Добавляем каждое сообщение к полю
            return self.form_invalid(form)
        form.save(self.request.user)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка при изменении пароля. Проверьте данные.')
        return super().form_invalid(form)
