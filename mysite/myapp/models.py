from click import option
from django.db import models
from django.db.models import CharField
from rest_framework.authtoken.admin import User
from rest_framework.viewsets import ModelViewSet

class User(models.Model):
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=50)
    email = models.EmailField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)


class Project(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=15)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)

    def __str__(self):
        print (f"{ self.owner }")
