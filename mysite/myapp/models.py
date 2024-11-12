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
    # members = models.ManyToManyField()

    def __str__(self):
        print (f"{ self.owner }")

class User(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=50)

    def __str__(self):
        print (f"{ self.username }")


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# class MySetPasswordForm(SetPasswordForm):
#
#     def send_email(self, to_mail):
#         subject = 'Password changed successfully'
#         body = 'Your password has been changed successfully'
#         email = EmailMultiAlternatives(subject, body, None, [send_mail()])
#         email.send()
#
#     def save(self, commit=True):
#         if commit:
#             email = email_field_name = User.get_email_field_name()
#             user_email = getattr(self.user, email_field_name)
#             self.send_email(user_email)
#         super().save_(commit=commit)