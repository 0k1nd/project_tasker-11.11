from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from rest_framework import response
from rest_framework.authtoken.admin import User
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .forms import UserForgotPasswordForm, UserSetNewPasswordForm


class RegistrationAPIView(APIView):

  def post(self, request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
      user = serializer.save()
      refresh = RefreshToken.for_user(user)
      return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
      }, status=status.HTTP_201_CREATED)

class TokenObtainPairView(APIView):
  permission_classes = (AllowAny,)
  serializer_class = UserSerializer

  def post(self, request, *args, **kwargs):
    email = request.data.get('email')
    password = request.data.get('password')

    if email and password:
      user = User.objects.filter(email=email).first()
      refresh = RefreshToken.for_user(user)
      return response.Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
      })
    return response.Response({'error': 'Поля email и пароль обязательны!'}, status=status.HTTP_401_UNAUTHORIZED)

class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):
  form_class = UserForgotPasswordForm
  template_name = 'system/user_password_reset.html'
  success_url = reverse_lazy('home')
  success_message = 'Письмо с инструкцией по восстановлению пароля отправлена на ваш email'
  subject_template_name = 'system/email/password_subject_reset_mail.txt'
  email_template_name = 'system/email/password_reset_mail.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = 'Запрос на восстановление пароля'
    return context

class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
  form_class = UserSetNewPasswordForm
  template_name = 'system/user_password_set_new.html'
  success_url = reverse_lazy('home')
  success_message = 'Пароль успешно изменен. Можете авторизоваться на сайте.'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = 'Установить новый пароль'
    return context