from django.contrib import admin
from .models import Project, Member, ProjectAdmin, Task, Comment

class ProjectAdminInline(admin.TabularInline):
    model = Member
    extra = 1

class ProjectAdminView(admin.ModelAdmin):
    inlines = [ProjectAdminInline]
    list_display = ('name', 'description', 'created_at')
    search_fields = ['name', 'description']

admin.site.register(Project, ProjectAdminView)
admin.site.register(Member)
admin.site.register(ProjectAdmin)

@admin.register(Task)
class TaskAdmin(ModelAdmin):
    pass

@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    pass

