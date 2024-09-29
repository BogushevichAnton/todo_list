from django.shortcuts import render

from todo_list.models import Note
from rest_framework import generics

from .serializers import NoteSerializer

# Create your views here.

class NotesAPIView(generics.ListAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer