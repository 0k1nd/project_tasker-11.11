from rest_framework.serializers import ModelSerializer
from rest_framework import  serializers
from myapp.models import Task, Comment, Project, Account


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = ['username', 'email']


class ProjectTaskSerializer(ModelSerializer):
    tasks = TaskSerializer(many=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'tasks','editors', 'description']
        annotated_tasks = serializers.IntegerField(read_only=True)

    def get_tasks(self):
        return Task.objects.filter(project=model.id)


class ProjectUserSerializer(ModelSerializer):
    editors = AccountSerializer(many=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'editors']

    def get_editors(self):
        return Account.objects.filter(project=model.id)


class ProjectSerializer(ModelSerializer):
    projects_task = serializers.IntegerField(read_only=True)
    projects_user = serializers.IntegerField(read_only=True)
    class Meta:
        model = Project
        fields = ['id', 'name', 'description','projects_task', 'projects_user', 'owner']

class TaskCommentSerializer(ModelSerializer):
    comments = CommentSerializer(many=True)

    class Meta:
        model = Task
        fields = '__all__'

    def get_editors(self):
        return Account.objects.filter(comments=model.id)
