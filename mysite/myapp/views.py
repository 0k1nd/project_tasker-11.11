from rest_framework import status, response
from rest_framework.authtoken.admin import User
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken

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
      if user and user.check_password(password):
        refresh = RefreshToken.for_user(user)
        return response.Response({
          'refresh': str(refresh),
          'access': str(refresh.access_token),
        })
      return response.Response({'error': 'Укажите правильный пароль или почту'}, status=status.HTTP_401_UNAUTHORIZED)

    return response.Response({'error': 'Поля email и пароль обязательны'}, status=status.HTTP_401_UNAUTHORIZED)