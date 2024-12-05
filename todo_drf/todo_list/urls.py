from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", views.index, name="index"),
    path('categories/', login_required(views.Category.as_view()), name='categories'),
    path('categories/add/', login_required(views.CategoryCreateView.as_view()), name='add_categories'),
    path('category/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
    path('categories/<int:pk>/', login_required(views.CategoryView.as_view()), name='view_category'),
    path('categories/<int:cat_id>/add_notes/', login_required(views.NotesCreateView.as_view()), name='add_notes'),
    path('categories/<int:cat_id>/delete_note/<int:pk>/', login_required(views.DeleteNotesView.as_view()), name='del_note'),
    path('categories/<int:cat_id>/update_note/<int:pk>/', login_required(views.UpdateNoteView.as_view()), name='update_note'),
]