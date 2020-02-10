                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
from django.db import models
from django.contrib.auth import get_user_model


class Registration(models.Model):
    
    fullname = models.CharField(max_length = 100)
    username = models.CharField(max_length = 100)
    email = models.EmailField()
    password = models.CharField(max_length = 100)
    password2 = models.CharField(max_length = 100)

    def __str__(self):
        return self.username
