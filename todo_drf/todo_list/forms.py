from django import forms
from .models import Note, Categories

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'deadline', 'color']  # Убрали category из поля
