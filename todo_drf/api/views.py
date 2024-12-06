from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from authuser.models import User
from todo_list.models import Note, Categories

from rest_framework import permissions, viewsets

from .serializers import NoteSerializer, CategorySerializer


class NotesViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    basename = 'notes'

    def get_queryset(self):
        """
        Возвращает список заметок для текущего пользователя.
        """
        user = self.request.user
        return Note.objects.select_related('category').filter(category__user=user)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    basename = 'categories'

    def get_queryset(self):
        """
        Возвращает список категорий для текущего пользователя.
        """
        user = self.request.user
        return Categories.objects.filter(user=user).order_by('id')

    def perform_create(self, serializer):
        # Автоматически добавляем пользователя при создании
        serializer.save(user=self.request.user)
