from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, CommentViewSet, ProjectViewSet
from . import views_2
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="W",
        default_version='v1',
        description="супер-мега крутое описание",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'projects', ProjectViewSet, basename='allprogects')


urlpatterns = [
    path('projects/<int:pk>/detail/', views_2.project_detail, name='project_detail'),
    path('projects/<int:pk>/tasks/', views_2.project_task, name='project_task'),
    path('projects/<int:pk>/create_task/', views_2.project_task, name='project_create_task'),
    path('task/<int:pk>/actions/', views_2.task_actions, name='task_detail'),
    path('tasks/<int:pk>/change_status/', views_2.change_status, name='task_change_status'),
    path('tasks/<int:pk>/change_assign/', views_2.change_assign, name='task_change_assign'),
    path('tasks/<int:pk>/task_comments/', views_2.task_comments, name='task_comments'),
    path('tasks_report/', views_2.tasks_report, name='tasks_report'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += router.urls
