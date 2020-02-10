from django.db import models
from django.contrib.auth.models import User

class Label(models.Model):
    user_id = models.ForeignKey(User, related_name='Label_owner', on_delete=models.CASCADE)
    label = models.CharField(max_length=50, blank=True)

    def __str__(self):  
        return str(self.label)

class Note(models.Model):
    user = models.ForeignKey(User, related_name='Note_owner', on_delete=models.CASCADE)
    title = models.CharField(max_length=60, blank=True)
    note = models.TextField(blank=True)
    label = models.ManyToManyField(Label, blank=True)
    add_picture = models.ImageField(upload_to='images/', blank=True, null=True)
    is_archived = models.BooleanField(default=False)
    is_bin = models.BooleanField(default=False)
    color = models.CharField(max_length=16, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)
    is_pinned = models.BooleanField(default=False)
    more = models.URLField(blank=True, null=True)
    reminder = models.DateTimeField(blank=True, null=True)
    collaborators = models.ManyToManyField(User, blank=True)
    def __str__(self):
        return str(self.user)
