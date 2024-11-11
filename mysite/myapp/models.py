from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


STATUS_CHOICES =(
    (1, "new"),
    (2, "in_progress"),
    (3, "done"),
)

class Task(models.Model):
    #project = models.ManyToManyField(Project)
    title = models.CharField(max_length=150)
    description = models.TextField()
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES)
    assignee = models.ForeignKey(User, models.SET_NULL,blank=True,null=True)
    created_at = models.DateTimeField(blank=True, null=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}  {self.status}'


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    author = models.ForeignKey(User, models.SET_NULL,blank=True,null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)