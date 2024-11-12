
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from myapp.views import TaskViewSet, CommentViewSet, ProjectCommentViewSet

router = SimpleRouter()
router.register(r'tasks', TaskViewSet, basename='user')
router.register(r'comments', CommentViewSet)
router.register(r'projects', ProjectCommentViewSet)
urlpatterns = [
]

urlpatterns += router.urls
