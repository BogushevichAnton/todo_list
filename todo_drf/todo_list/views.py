from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView

from django.http import Http404
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from todo_list.forms import NoteForm
from todo_list.models import Note, Categories
from django.db import IntegrityError

from django.db.models import F
from django.db.models.functions import Lower


def get_user_categories(self :None):
    return Categories.objects.filter(user=self.request.user).select_related('user')

def index(request):
    if request.user.is_authenticated == True:
        categories_list = Categories.objects.filter(user=request.user).select_related('user')
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
            raise Http404('Такая страница не существует')

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
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs['pk']
        page_number = self.request.GET.get('page')

        notes = Note.objects.filter(category=category_id).order_by(
            '-color', 'published_date', 'title'
        )

        paginator = Paginator(notes, self.paginate_by)

        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.get_page(1)
        except EmptyPage:
            page_obj = paginator.get_page(paginator.num_pages)

        # Применяем аннотацию только к страницам, которые мы отображаем. Это ключевое изменение для оптимизации.
        annotated_page_obj = page_obj.object_list.annotate(color_order=Lower(F('color')))

        context['notes'] = [{
            'note': note,
            'time_left': note.time_left,
        } for note in annotated_page_obj]
        context['page_obj'] = page_obj
        context['is_paginated'] = page_obj.has_other_pages()
        context['last_page'] = paginator.num_pages
        context['colors'] = {
            'red': 'table-danger',
            'green': 'table-success',
            'orange': 'table-warning',
        }
        context['categories_list'] = get_user_categories(self)
        return context

class DeleteNotesView(DeleteView):
    model = Note
    template_name = 'todo_list/note_delete.html'
    def get_success_url(self):
        return reverse_lazy('view_category', kwargs={'pk': self.object.category.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat_id'] = self.kwargs['cat_id']  # Получаем cat_id из URL
        return context

class UpdateNoteView(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'todo_list/note_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_id = self.kwargs.get('cat_id')
        note_id = self.kwargs.get('pk')
        try:
            context['category'] = Categories.objects.get(pk=cat_id)
            context['note'] = Note.objects.get(pk=note_id)
        except Categories.DoesNotExist:
            raise Http404('Страница не существует')
        context['categories_list'] = get_user_categories(self)
        return context

    def form_valid(self, form):
        note = form.save(commit=False)
        note.category = Categories.objects.get(pk=self.kwargs.get('cat_id'))
        note.save()

        return redirect(reverse_lazy('view_category', kwargs={'pk':self.kwargs.get('cat_id')}))


class CategoryDeleteView(DetailView):
    model = Categories
    template_name = 'todo_list/category_delete.html'
    success_url = reverse_lazy('categories')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object

        notes = Note.objects.filter(category=category).order_by(
            '-color', 'published_date', 'title'
        )

        paginator = Paginator(notes, 4)  # 25 заметок на странице
        page_number = self.request.GET.get('page')
        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.get_page(1)
        except EmptyPage:
            page_obj = paginator.get_page(paginator.num_pages)
        annotated_page_obj = page_obj.object_list.annotate(color_order=Lower(F('color')))

        context['category'] = category
        context['page_obj'] = page_obj
        context['notes'] = annotated_page_obj
        context['is_paginated'] = page_obj.has_other_pages()
        context['last_page'] = paginator.num_pages
        context['categories_list'] = get_user_categories(self)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.success_url)