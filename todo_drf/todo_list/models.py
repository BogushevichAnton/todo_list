from django.db import models
''' Файл для Тани '''
# Create your models here.

class Note(models.Model):
    title = models.CharField(max_length=255, verbose_name='Тип тут будет наша заметка')

    def __str__(self):
        return self.title
