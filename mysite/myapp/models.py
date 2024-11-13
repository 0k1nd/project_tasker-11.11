from django.conf import settings
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import AbstractUser
from django.core.mail import EmailMultiAlternatives, send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.admin import User
from rest_framework_simplejwt.tokens import Token

class Project(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=15)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)

    def __str__(self):
        print (f"{ self.owner }")