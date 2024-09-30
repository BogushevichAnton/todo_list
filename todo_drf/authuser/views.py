from django.http import HttpResponse
from django.shortcuts import render, redirect

from authuser.forms import AuthForm


# Create your views here.
def auth(request):
    if request.method == 'POST':
        return redirect('index')
    else:
        form = AuthForm()
    return render(request, 'authuser/auth.html', {'form': form})

def register(request):
    return render(request, 'authuser/register.html')

