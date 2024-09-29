from django.http import HttpResponse
from django.shortcuts import render
''' Файл для Володи '''



def index(request):
    '''Коннект к бд'''

    data = {'словарь1': 123}
    return render(request, 'todo_list/index.html',
                  {'data': data, }
                  )
