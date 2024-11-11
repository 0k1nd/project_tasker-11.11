from django.urls import path, include
from rest_framework.routers import SimpleRouter
from myapp.views import TaskViewSet, CommentViewSet

router = SimpleRouter()
router.register(r'tasks', TaskViewSet, basename='user')
router.register(r'comments', CommentViewSet)

urlpatterns = [
]

urlpatterns += router.urls
