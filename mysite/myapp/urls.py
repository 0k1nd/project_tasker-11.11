from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView
from .views import RegistrationAPIView, TokenObtainPairView, UserForgotPasswordView, UserPasswordResetConfirmView, \
    ProjectView, edit_project

app_name = "user"

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name="register"),
    path('login/', TokenObtainPairView.as_view(), name="login"),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('password-reset/', UserForgotPasswordView.as_view(), name='password_reset'),
    path('set-new-password/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('project/', ProjectView.as_view(), name='project'),
    path('project/<int:project_id>/edit/', edit_project, name='edit_project'),
]

