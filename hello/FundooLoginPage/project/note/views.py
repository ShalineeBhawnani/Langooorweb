from note.models import Note,Label
from note.serializer import LabelSerializer,NoteSerializer,SearchNoteSerializer,NoteFunctionSerializer
from rest_framework import mixins
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User


@method_decorator(login_required, name='dispatch')
class CreateLabel(generics.GenericAPIView,
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    serializer_class=LabelSerializer
    
    lookup_field='id'
    
    def get(self,request,id=None):     
        # print(request.user)
        # print(request.user.id)
        queryset =  Label.objects.filter(user_id=request.user.id)
        if id:
            return self.retrieve(request,id)
        else:
            return self.list(request)
            
    def post(self, request, *args, **kwargs):
        return self.create(self.request)
    
    def perform_create(self,serializer):
        serializer.save(user_id=self.request.user)
        

    def put(self,request,id=None):
        print("editated")
        return self.update(request,id)
        
    def delete(self,request,id=None):
        return self.destroy(request,id)
    
@method_decorator(login_required, name='dispatch')
class CreateNote(generics.GenericAPIView,
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    serializer_class=NoteSerializer
    queryset = Note.objects.all()
    lookup_field='id'
    
    def get(self,request,id=None):
        if id:
            return self.retrieve(request,id)
        else:
            return self.list(request)
            
    def post(self, request, *args, **kwargs):
        return self.create(self.request)
    
    # def perform_create(self,serializer):
    #     serializer.save(user_id=self.request.user)
        

    def put(self,request,id=None):
        print("editated")
        return self.update(request,id)
        
    def delete(self,request,id=None):
        return self.destroy(request,id)
    

        
        