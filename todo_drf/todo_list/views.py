from django.views.generic import ListView, CreateView

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from todo_list.models import Note, Categories
from django.db import IntegrityError

''' Файл для Володи '''


def index(request):
    '''Коннект к бд'''
    return render(request, 'todo_list/index.html', )


class Category(ListView):
    model = Categories
    template_name = 'todo_list/topics.html'

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Categories.objects.filter(user=self.request.user).select_related('user').prefetch_related('notes')




def check_status_category_name(self, name: str) -> bool:
    ''' Имя категории проверятся без учета регистра, т.е. Работа == РаБоТа '''
    # Результат - True or False
    categories_user = Categories.objects.filter(user=self.request.user).select_related('user').values_list('name', flat=True)
    if name.lower() in tuple(map(lambda x: x.lower(), categories_user)):
        return False
    return True



class CategoryCreateView(CreateView):
    model = Categories
    fields = ['name']
    template_name = 'todo_list/category_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            if check_status_category_name(self, form.instance.name):
                return super().form_valid(form)
            raise IntegrityError

        except IntegrityError as unique_error:
            form.add_error('name', 'Не удалось создать категорию, такая категория уже существует. Категории проверяются без учета регистра')
            return super().form_invalid(form)

        except Exception as e:
            form.add_error('name', 'Не удалось создать категорию.')
            return super().form_invalid(form)

    def get_success_url(self):
        return reverse('categories')



def delete_category(request, cat_id):
    """Удаляет категорию по её ID."""
    category = Categories.objects.get(pk=cat_id)
    notes = Note.objects.filter(category=cat_id)

    if request.method == 'POST':
        category.delete()
        return redirect('categories')  # Перенаправление на список категорий

    # Отображение формы подтверждения удаления
    context = {
        'category': category,
        'notes': notes,

    }
    return render(request, 'todo_list/category_delete.html', context)



