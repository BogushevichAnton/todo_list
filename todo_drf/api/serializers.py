from rest_framework.serializers import ModelSerializer
from todo_list.models import Note

class NoteSerializer(ModelSerializer):
    class Meta:
        model = Note
        fields = ('title', )
