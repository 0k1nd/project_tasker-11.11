from django.contrib.auth import get_user_model
from rest_framework import status, response
from rest_framework.authtoken.admin import User
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegistrationSerializer

User = get_user_model()

class RegisterView(APIView):
  queryset = User.objects.all()
  permission_classes = (AllowAny,)
  serializer_class = RegistrationSerializer

@api_view(['POST',])
def registration_view(self, request):

  if request.method == 'POST':
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
      user = serializer.save()
      data['response'] = "successfully registered a new user."
      data['email'] = user.email
      data['username'] = user.username
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
      data = serializer.errors
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
  @classmethod
  def get_token(cls, user):
    token = super(MyTokenObtainPairSerializer, cls).get_token(user)
    token['username'] = user.username
    return token


class TokenObtainPairView(APIView):
  permission_classes = (AllowAny,)
  serializer_class = RegistrationSerializer

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

    return response.Response({'error': 'Error'}, status=status.HTTP_401_UNAUTHORIZED)