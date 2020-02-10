from rest_framework import serializers
from .models import Note,Label
from django.contrib.auth.models import User

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = '__all__'
     
        # read_only_fields = ['user']

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'
        #read_only_fields = ['user']

class SearchNoteSerializer(serializers.ModelSerializer):
    class Meta:

        model = Note
        fields = ['title', 'note', 'reminder', 'color', 'label']

class NoteFunctionSerializer(serializers.ModelSerializer):
    
    class Meta:

        model = Note
        fields = ['title', 'note', 'label','add_picture', 'is_archived', 'is_bin', 'color',
                  'is_pinned', 'more', 'reminder', 'collaborators']
        

class LabelFunctionSerializer(serializers.ModelSerializer):
    
    class Meta:

        model = Note
        fields = ['label']
