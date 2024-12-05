"""
URL configuration for todo_drf project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from authuser.views import Register, Auth, logout_view, profile, ChangeUsernameView, PasswordChangeView
from debug_toolbar.toolbar import debug_toolbar_urls


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('todo_list.urls')),
    path("login/", Auth.as_view(), name='login'),
    path("logout/", logout_view, name='logout'),
    path("register/", Register.as_view(), name="register"),



    path('api/v1/', include('api.urls')),
    path('profile/', login_required(profile), name='profile'),
    path('profile/update_name/',  login_required(ChangeUsernameView.as_view()), name='profile_update_name'),
    path('profile/password/', login_required(PasswordChangeView.as_view()), name='password_update'),


] + debug_toolbar_urls()
