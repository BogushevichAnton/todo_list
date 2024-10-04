from django.urls import path, include
from .views import NotesAPIView

urlpatterns = [
    # ex: /polls/
    path("", NotesAPIView.as_view(), name="apiView"),
    path("api-auth/", include('rest_framework.urls')),
]