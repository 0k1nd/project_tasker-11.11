from django.shortcuts import render
from rest_framework import generics

from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer
from .models import Project
from .forms import UserRegistrationForm

token = Token.objects.create(user=...)
print(token.key)

class ProjectViewSet(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
        else:
            form = UserRegistrationForm()
    return render(request, 'accounts/register', {'form': form})