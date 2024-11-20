from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenVerifyView
from .views import RegistrationAPIView, TokenObtainPairView, edit_project, list_projects, create_project, project_detail, update_project, delete_project, AddMemberView, RemoveMemberView, ListMemberView, ProjectSummaryView, TaskViewSet
from .views import TaskViewSet
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from . import views_2

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)


urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name="register"),
    path('accounts/login/', TokenObtainPairView.as_view(), name="login"),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('project/<int:project_id>/edit/', edit_project, name='edit_project'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('projects/', list_projects, name='list_projects'),
    path('projects/create/', create_project, name='create_project'),
    path('projects/<int:pk>/', project_detail, name='project_detail'),
    path('projects/<int:pk>/update/', update_project, name='update_project'),
    path('projects/<int:pk>/delete/', delete_project, name='delete_project'),
    path('projects/<int:id>/add_member/', AddMemberView.as_view(), name='add_member'),
    path('projects/<int:id>/remove_member/', RemoveMemberView.as_view(), name='remove_member'),
    path('projects/<int:id>/members/', ListMemberView.as_view(), name='list_members'),
    path('projects/summary/<int:id>/', ProjectSummaryView.as_view(), name='project_summary_by_status'),
    path('projects/<int:pk>/detail/', views_2.project_detail, name='project_detail'),
    path('projects/<int:pk>/tasks/', views_2.project_task, name='project_task'),
    path('projects/<int:pk>/create_task/', views_2.project_task, name='project_create_task'),
    path('task/<int:pk>/actions/', views_2.task_actions, name='task_detail'),
    path('tasks/<int:pk>/change_status/', views_2.change_status, name='task_change_status'),
    path('tasks/<int:pk>/change_assign/', views_2.change_assign, name='task_change_assign'),
    path('tasks/<int:pk>/task_comments/', views_2.task_comments, name='task_comments'),
    path('tasks_report/', views_2.tasks_report, name='tasks_report')
]

urlpatterns += router.urls




