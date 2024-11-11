from os import path

from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserRegistrationForm
from .views import MyObtainTokenPairView
from rest_framework.authtoken import views


urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='login'),
    path('register/', UserRegistrationForm, name='register')
]