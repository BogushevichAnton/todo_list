from django.views.generic import ListView, CreateView, DeleteView, DetailView

from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from unicodedata import category
from django.core import serializers
from todo_list.forms import NoteForm
from todo_list.models import Note, Categories
from django.db import IntegrityError

from django.db.models import F, Value
from django.db.models.functions import Lower


def get_user_categories(self :None):
    return Categories.objects.filter(user=self.request.user).select_related('user').prefetch_related('notes')

def index(request):
    if request.user.is_authenticated == True:
        categories_list = Categories.objects.filter(user=request.user).select_related('user').prefetch_related('notes')
        context = {
            'categories_list': categories_list
        }
        return render(request, 'todo_list/index.html', context=context)
    return render(request, 'todo_list/index.html')


class Category(ListView):
    model = Categories
    template_name = 'todo_list/topics.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_list'] = get_user_categories(self)
        return context


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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_list'] = get_user_categories(self)
        return context



def delete_category(request, cat_id):
    """Удаляет категорию по её ID."""
    category = Categories.objects.get(pk=cat_id)
    notes = Note.objects.filter(category=cat_id)

    if request.method == 'POST':
        category.delete()
        return redirect('categories')  # Перенаправление на список категорий

    # Отображение формы подтверждения удаления
    categories_list = Categories.objects.filter(user=request.user).select_related('user').prefetch_related('notes')
    context = {
        'category': category,
        'notes': notes,
        'categories_list': categories_list

    }


    return render(request, 'todo_list/category_delete.html', context)

class NotesCreateView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'todo_list/note_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_id = self.kwargs.get('cat_id')
        try:
            context['category'] = Categories.objects.get(pk=cat_id)
        except Categories.DoesNotExist:
                #Здесь нужна обработка ошибок пока отсылка на 404, необходима страница загрузки ошибки
            raise Http404('hello')

        context['categories_list'] = get_user_categories(self)
        return context

    def form_valid(self, form):
        note = form.save(commit=False)
        note.category = Categories.objects.get(pk=self.kwargs.get('cat_id'))
        note.save()

        return redirect(reverse_lazy('view_category', kwargs={'pk':self.kwargs.get('cat_id')}))


class CategoryView(DetailView):
    model = Categories
    template_name = 'todo_list/category_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notes = Note.objects.filter(category=self.kwargs['pk']).annotate(
              color_order=Lower(F('color'))
            ).order_by(
              '-color_order',
              'published_date'
            )
        context['notes'] = [{
            'note': note,
            'time_left': note.time_left,
        } for note in notes]
        context['colors'] = {
            'red': 'table-danger',
            'green': 'table-success',
            'orange': 'table-warning',
        }
        context['categories_list'] = get_user_categories(self)
        return context




