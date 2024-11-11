from rest_framework.serializers import ModelSerializer

from mysite.myapp.models import Task


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ('__all__')