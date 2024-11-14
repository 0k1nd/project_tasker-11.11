from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, CommentViewSet, ProjectViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'projects', ProjectViewSet, basename='allprogects')


urlpatterns = [
]

urlpatterns += router.urls
