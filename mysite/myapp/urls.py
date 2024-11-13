from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView

from .forms import RegistrationForm
from .views import registration_view
from .views import TokenObtainPairView

app_name = "user"

urlpatterns = [
    path('register/', registration_view, name="register"),
    path('login/', TokenObtainPairView.as_view(), name="login"),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]


