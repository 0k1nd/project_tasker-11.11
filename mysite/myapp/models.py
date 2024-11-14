from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=50)

    def __str__(self):
        return f"id {self.id} {self.username}"

STATUS_CHOICES =(
    ('new', "new"),
    ('in_progress', "in_progress"),
    ('done', "done"),
)

class Project(models.Model):
    name = models.CharField(max_length=15)
    description = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    editors = models.ManyToManyField(Account, related_name='editable_objects', blank=True, null=True)


    def __str__(self):
        return f"{self.name} {self.editors}"




class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE,blank=True,null=True, related_name="tasks")
    name = models.CharField(max_length=150)
    description = models.TextField()
    status = models.TextField(choices=STATUS_CHOICES)
    assignee = models.ForeignKey(User, models.SET_NULL,blank=True,null=True)
    created_at = models.DateTimeField(blank=True, null=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}  {self.status}'


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, models.SET_NULL,blank=True,null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)