from django.views.generic import ListView

from django.http import HttpResponse
from django.shortcuts import render

from todo_list.models import Note

''' Файл для Володи '''



def index(request):
    '''Коннект к бд'''
    links = {
        'login': 'login/',
        'register': 'register/',
        'logout': 'logout/',
        'topics': 'topics/',
    }
    return render(request, 'todo_list/index.html',
                  {'links': links, }
                  )

class Topics(ListView):
    model = Note
    template_name = 'todo_list/topics.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Note.objects.all()
