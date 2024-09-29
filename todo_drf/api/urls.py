from django.urls import path
from .views import NotesAPIView

urlpatterns = [
    # ex: /polls/
    path("", NotesAPIView.as_view(), name="apiView"),
]