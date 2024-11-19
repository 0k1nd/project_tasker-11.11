from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenVerifyView
from .views import RegistrationAPIView, TokenObtainPairView, edit_project, list_projects, create_project, project_detail, update_project, delete_project, AddMemberView, RemoveMemberView, ListMemberView, ProjectSummaryView
from .views import TaskViewSet, CommentViewSet, ProjectViewSet, OneProjectViewSet
from django.contrib.auth import views as auth_views
from .views import CustomPasswordResetView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView
app_name = "user"

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'projects', ProjectViewSet, basename='allprogects')
router.register(r'project', OneProjectViewSet, basename='oneprogect')


urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name="register"),
    path('login/', TokenObtainPairView.as_view(), name="login"),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('project/<int:project_id>/edit/', edit_project, name='edit_project'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('projects/', list_projects, name='list_projects'),
    path('projects/create/', create_project, name='create_project'),
    path('projects/<int:pk>/', project_detail, name='project_detail'),
    path('projects/<int:pk>/update/', update_project, name='update_project'),
    path('projects/<int:pk>/delete/', delete_project, name='delete_project'),
    path('projects/<int:id>/add_member/', AddMemberView.as_view(), name='add_member'),
    path('projects/<int:id>/remove_member/', RemoveMemberView.as_view(), name='remove_member'),
    path('projects/<int:id>/members/', ListMemberView.as_view(), name='list_members'),
    path('projects/summary/<int:id>/', ProjectSummaryView.as_view(), name='project_summary_by_status'),
]

urlpatterns += router.urls




