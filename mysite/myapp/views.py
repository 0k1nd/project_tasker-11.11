from rest_framework.authtoken.admin import User
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegistrationSerializer

class RegisterView(APIView):
  queryset = User.objects.all()
  permission_classes = (AllowAny,)
  serializer_class = RegistrationSerializer
  @api_view(['POST',])

  def registration_view(request):

    if request.method == 'POST':
      serializer = RegistrationSerializer(data=request.data)
      data = {}
      if serializer.is_valid():
        user = serializer.save()
        data['response'] = "successfully registered a new user."
        data['email'] = user.email
        data['username'] = user.username
      else:
        data = serializer.errors
      return Response(data)