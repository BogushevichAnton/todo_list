from django.db import models

from authuser.models import User
from django.core.validators import MinLengthValidator
from django.utils import timezone

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
    description = models.CharField(max_length=255, verbose_name='Ваше описание')
    color = models.CharField(max_length=25, verbose_name='цвет заметки')

    # Дата публикации
    published_date = models.DateTimeField(auto_now_add=True, verbose_name='дата публикации')

    # Дедлайн
    deadline = models.DateTimeField(null=True, blank=True, verbose_name='дедлайн')

    # Цвет
    color_choices = [
        ('red', 'Красный'),
        ('orange', 'Оранжевый'),
        ('green', 'Зеленый'),
    ]
    color = models.CharField(max_length=10, choices=color_choices, default='green', verbose_name='цвет заметки')

    @property
    def time_left(self):
        if self.deadline:
            time_left = self.deadline - timezone.now()
            if time_left.days < 0:
                return "Просрочено"

            result = f''
            if time_left.days > 0:
                result += f"{time_left.days} дней "
            hours = time_left.seconds // 3600
            if hours > 0:
                result += f'{hours} часов '
            minutes = (time_left.seconds % 3600) // 60
            if minutes > 0:
                result += f'{minutes} минут'
            return result
        else:
            return "Нет дедлайна"

    def __str__(self):
        return self.title
