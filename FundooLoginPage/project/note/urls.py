from django.urls import path
from django.conf.urls import url, include
from note import views
from note.views import CreateLabel,CreateNote
# LabelListCreate,NoteListDetail,NoteListDelete,NoteListUpdate
from django.contrib.auth.decorators import login_required, permission_required



urlpatterns = [
    #path('note/', views.CreateNote.as_view() ,name="note"),
    path('note/<int:id>/', views.CreateNote.as_view() ,name="note"),
    path('label/<int:id>/', views.CreateLabel.as_view() ,name="label"),
    path('label/', views.CreateLabel.as_view() ,name="label"),

    # path('notedetails/<int:pk>/', views.NoteListDetail.as_view() ,name="note_details"),
    # path('notedelete/<int:pk>/', views.NoteListDelete.as_view() ,name="note_delete"),
    # path('noteupdate/<int:pk>/', views.NoteListUpdate.as_view() ,name="note_update"),


]

