from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django import forms
from django.contrib.auth.views import PasswordResetDoneView

from .models import Project, Member

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']
