from django.http import HttpResponse
from django.shortcuts import render
''' Файл для Володи '''



def index(request):
    '''Коннект к бд'''
    links = {
        'login': 'login/',
        'register': 'register/',
        'logout': 'logout/'
    }
    return render(request, 'todo_list/index.html',
                  {'links': links, }
                  )
