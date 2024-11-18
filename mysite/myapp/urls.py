from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, CommentViewSet, ProjectViewSet
from django.urls import path
from . import views_2

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'projects', ProjectViewSet, basename='allprogects')


urlpatterns = [
    path('projects/<int:pk>/detail/', views_2.project_detail, name='project_detail'),
    path('projects/<int:pk>/tasks/', views_2.project_task, name='project_task'),
    path('projects/<int:pk>/create_task/', views_2.project_task, name='project_create_task'),
    path('task/<int:pk>/actions/', views_2.task_actions, name='task_detail'),
    path('/tasks/<int:pk>/change_status/', views_2.change_status, name='task_change_status'),
]

urlpatterns += router.urls
