from os import path

from rest_framework_simplejwt.views import TokenRefreshView

from .views import MyObtainTokenPairView
from rest_framework.authtoken import views


urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]