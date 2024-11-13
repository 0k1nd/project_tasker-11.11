from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.admin import User
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegistrationSerializer

User = get_user_model()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
  @classmethod
  def get_token(cls, user):
    token = super(MyTokenObtainPairSerializer, cls).get_token(user)
    token['username'] = user.username
    return token

class ObtainTokenPairView(TokenObtainPairView):
  serializer_class = MyTokenObtainPairSerializer

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

  class CustomTokenObtainPairView(TokenObtainPairView):
    pass