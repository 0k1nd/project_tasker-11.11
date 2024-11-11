from django.db import models
from django.db.models import CharField
from rest_framework.authtoken.admin import User
from rest_framework.viewsets import ModelViewSet


class Project(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=15)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
