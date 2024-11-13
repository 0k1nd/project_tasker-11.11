from django import forms

from myapp.models import Task, Project

from django import forms

class PostFormProject(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'editors')

class PostForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'description', 'status')