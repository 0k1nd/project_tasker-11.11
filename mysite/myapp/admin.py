from django.contrib import admin
from django.contrib.admin import ModelAdmin
from myapp.models import Task, Project, Comment, Account


@admin.register(Task)
class TaskAdmin(ModelAdmin):
    pass

@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    pass

@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    pass

@admin.register(Account)
class AccountAdmin(ModelAdmin):
    pass