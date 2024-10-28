from django.db import models

from authuser.models import User
from django.core.validators import MinLengthValidator

''' Файл для Тани '''
# Create your models here.

class Categories(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=16, verbose_name='наименование категории', validators=[MinLengthValidator(2)])
    class Meta:
        unique_together = ('user', 'name')
    def __str__(self):
        return self.name

class Note(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=255, verbose_name='наименование заметки')
    color = models.CharField(max_length=25, verbose_name='цвет заметки')

    def __str__(self):
        return self.title
