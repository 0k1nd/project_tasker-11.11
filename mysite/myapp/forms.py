from django import forms
from django.contrib.auth.views import SetPasswordForm, PasswordResetForm

from .models import Project, Member

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']