from django.urls import path
from .views import registration_view

app_name = "user"

urlpatterns = [
    path('register', registration_view, name="register")
]


# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )