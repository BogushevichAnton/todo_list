from django import forms
from .models import Note, Categories

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'description', 'deadline', 'color']

    def __init__(self, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Наименование заметки'
        })

        self.fields['deadline'].widget.attrs.update({
            'class': 'form-control',
            'id': 'datetimepicker',
            'placeholder': 'Выберите дату дедлайна',
            'type': 'date'  # Пример указания типа для виджета
        })

        self.fields['color'].widget.attrs.update({
            'class': 'form-select',
        })

        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Описание заметки'
        })
