from rest_framework.routers import DefaultRouter

from .views import TaskViewSet, CommentViewSet, ProjectCommentViewSet
#from .routers import CustomRouter

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'projects', ProjectCommentViewSet)
urlpatterns = [
]

urlpatterns += router.urls
