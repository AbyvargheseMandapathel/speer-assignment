from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

# Create your models here.

class CustomUser(AbstractUser):
    pass

class Note (models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser , on_delete=models.CASCADE)
    shared_users = models.ManyToManyField(CustomUser, related_name='shared_notes', blank=True)
    
    def __str__(self):
        return self.title