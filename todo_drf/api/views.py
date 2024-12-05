from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from authuser.models import User
from todo_list.models import Note, Categories

from rest_framework import permissions, viewsets

from .serializers import NoteSerializer, CategorySerializer

# Create your views here.

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


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


    # perform_create - метод только для сохранения объекта. Для переадресации юзать create
    def perform_create(self, serializer):
        # Автоматически добавляем пользователя при создании
        serializer.save(user=self.request.user)


        # @action(detail=False, methods=['get'])
    # def my_categories(self, request):
    #     """
    #     Возвращает список категорий для текущего пользователя.
    #     """
    #     queryset = self.get_queryset()
    #     serializer = CategorySerializer(queryset, many=True)
    #     return Response(serializer.data)