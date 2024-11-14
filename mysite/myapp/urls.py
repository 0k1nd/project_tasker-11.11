from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, CommentViewSet, ProjectViewSet, OneProjectViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'projects', ProjectViewSet, basename='allprogects')
router.register(r'project', OneProjectViewSet, basename='oneprogect')


urlpatterns = [
]

urlpatterns += router.urls
