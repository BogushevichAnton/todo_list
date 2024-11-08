from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView
from rest_framework.reverse import reverse_lazy, reverse

from authuser.forms import AuthForm, RegisterForm


# Create your views here.
class Auth(LoginView):
    form_class = AuthForm
    template_name = 'authuser/login.html'

    def get_success_url(self):
         return reverse_lazy('index')

    # def get(self, request):
    #     form = self.form_class()
    #     return render(request, self.template_name, context={'form': form})
    #
    # def post(self, request, *args, **kwargs):
    #     email = request.POST['email']
    #     password = request.POST['password']
    #     user = authenticate(request, email=email, password=password)
    #     if user is not None:
    #         login(request, user)
    #         return redirect('index')
    #     else:
    #         form = self.form_class()
    #         return render(request, self.template_name, context={'form': form,
    #                                                             'error': 'Неверное имя пользователя или пароль'}
    #                       )

        # ''' Вроде как дальше юзать для api '''
        #response = HttpResponse(get_token(request))
        #return response

@login_required
def logout_view(request):
    logout(request)
    return redirect('index')



class Register(CreateView):
    form_class = RegisterForm
    template_name = "authuser/register.html"

    def get_success_url(self):
        return reverse_lazy('index')

    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)
        return super().form_valid(form)

