from django.http import HttpResponse
from django.shortcuts import render
''' Файл для Володи '''



def index(request):
    '''Коннект к бд'''
    links = {
        'auth': '../auth',
        'register': '../register',
    }
    return render(request, 'todo_list/index.html',
                  {'links': links, }
                  )
