from django.utils import timezone
from django.db import models

from rest_framework.authtoken.admin import User

class Project(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=15)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    editors = models.ManyToManyField(User, related_name='editable_objects', blank=True, null=True)

    def __str__(self):
        return f"{ self.name }"

class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='members', on_delete=models.CASCADE)
    role = models.CharField(max_length=100, choices=[('Admin', 'Admin'), ('Member', 'Member')], default='Member')

    def __str__(self):
        return f'{self.user.username} - {self.project.name}'

class ProjectAdmin(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - Создатель: {self.project.name}'

    def has_permission_to_edit(self):
        return self.is_admin

    def has_permission_to_delete(self):
        return self.is_admin

    def has_permission_to_manage_participants(self):
        return self.is_admin


STATUS_CHOICES =(
    ('new', "new"),
    ('in_progress', "in_progress"),
    ('done', "done"),
)

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
