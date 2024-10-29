from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", views.index, name="index"),
    path('categories/', login_required(views.Category.as_view()), name='categories'),
    path('categories/add/', login_required(views.CategoryCreateView.as_view()), name='add_categories'),
    path('categories/delete/<int:cat_id>/', views.delete_category, name='delete_category'),
    path('categories/<int:pk>/', login_required(views.CategoryView.as_view()), name='view_category'),
    path('categories/<int:cat_id>/add_notes/', login_required(views.NotesCreateView.as_view()), name='add_notes'),
]