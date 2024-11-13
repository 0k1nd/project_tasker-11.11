from django.db import models
from rest_framework.authtoken.admin import User

class Project(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=15)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)

    def __str__(self):
        print (f"{ self.owner }")