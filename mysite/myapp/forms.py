from django import forms
from django.contrib.auth.models import User
from .models import Project

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)