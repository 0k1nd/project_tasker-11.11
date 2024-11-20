from django.utils import timezone
from django.db import models

from rest_framework.authtoken.admin import User

class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, choices=[('Admin', 'Admin'), ('Member', 'Member')], default='Member')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.username} - {self.project.name}'

class Project(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=15)
    description = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    editors = models.ManyToManyField(Member, related_name='editable_objects', blank=True, null=True)

    def __str__(self):
        return f"{ self.name }"


STATUS_CHOICES =(
    ('new', "new"),
    ('in_progress', "in_progress"),
    ('done', "done"),
)

class Task(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='id')
    project = models.ForeignKey(Project, on_delete=models.CASCADE,blank=True,null=True, related_name="tasks")
    name = models.CharField(max_length=150)
    description = models.TextField()
    status = models.CharField(max_length=150, choices=STATUS_CHOICES)
    assignee = models.ManyToManyField(Member, related_name='pined_task', blank=True,null=True)
    created_at = models.DateTimeField(blank=True, null=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}  {self.status}'

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(Member, models.SET_NULL,blank=True,null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    
