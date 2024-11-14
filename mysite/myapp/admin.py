from django.contrib import admin
from .models import Project, Member, ProjectAdmin


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