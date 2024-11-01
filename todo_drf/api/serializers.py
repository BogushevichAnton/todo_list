from rest_framework import serializers

from authuser.models import User
from todo_list.models import Note, Categories


class NoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'title', )

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'email', 'name']



class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Categories
        fields = ('id', 'name', )
