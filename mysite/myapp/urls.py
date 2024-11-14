
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
]

urlpatterns += router.urls



