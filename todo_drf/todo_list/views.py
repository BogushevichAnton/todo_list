from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    '''Коннект к бд'''
    ''' Тут что то меняем в данных '''
    ''' бд -> данные парсим в dict '''
    data = {'словарь1': 123}
    return render(request, 'todo_list/index.html',
                  {'data': data, }
                  )
