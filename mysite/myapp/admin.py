from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Project, Member, Task, Comment

admin.site.register(Project)
admin.site.register(Member)

@admin.register(Task)
class TaskAdmin(ModelAdmin):
    pass

@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    pass

