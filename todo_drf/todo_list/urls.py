from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", views.index, name="index"),
    path('topics/', login_required(views.Topics.as_view()), name='topics'),
]