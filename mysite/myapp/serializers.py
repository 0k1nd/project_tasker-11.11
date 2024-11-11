from rest_framework.serializers import ModelSerializer

from myapp.models import Task, Comment


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ('__all__')

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ('__all__')