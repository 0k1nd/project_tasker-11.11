import self
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from pywin.mfc.object import Object
from .models import Project, Registration, Login
from social_core.pipeline import user


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ('username', 'email', 'password')

    email = forms.EmailField(label='email', widget=forms.EmailInput)
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='repeat password', widget=forms.PasswordInput)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = self.cleaned_data['password']
        user.set_password(user.password)
        if commit:
            user.save()
        return user


class LoginForm(forms.ModelForm):
    class Meta:
        model = Login
        fields = ('username', 'email', 'password')

    email = forms.EmailField(label='email', widget=forms.EmailInput)
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='repeat password', widget=forms.PasswordInput)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = self.cleaned_data['password']
        user.set_password(user.password)
        if commit:
            user.save()
        return user