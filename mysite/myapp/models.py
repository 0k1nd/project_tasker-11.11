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
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.title}  {self.status}'
