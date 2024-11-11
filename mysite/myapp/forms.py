from django import forms

from mysite.myapp.models import Task


class PostForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'status')