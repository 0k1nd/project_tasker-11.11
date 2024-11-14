
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenVerifyView
from .views import RegistrationAPIView, TokenObtainPairView, UserForgotPasswordView, UserPasswordResetConfirmView, \
    ProjectView, edit_project
from .views import TaskViewSet, CommentViewSet, ProjectViewSet, OneProjectViewSet
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
    path('password-reset/', UserForgotPasswordView.as_view(), name='password_reset'),
    path('set-new-password/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('project/', ProjectView.as_view(), name='project'),
    path('project/<int:project_id>/edit/', edit_project, name='edit_project'),
    path('projects/', list_projects, name='list_projects'),
    path('projects/create/', create_project, name='create_project'),
    path('projects/<int:pk>/', project_detail, name='project_detail'),
    path('projects/<int:pk>/update/', update_project, name='update_project'),
    path('projects/<int:pk>/delete/', delete_project, name='delete_project'),
    path('projects/<int:id>/add_member/', AddMemberView.as_view(), name='add_member'),
    path('projects/<int:id>/remove_member/', RemoveMemberView.as_view(), name='remove_member'),
    path('projects/members/', ListMemberView.as_view(), name='list_members'),
    path('projects/<int:id>/summary/', ProjectSummaryView.as_view(), name='project_summary'),
]

urlpatterns += router.urls



