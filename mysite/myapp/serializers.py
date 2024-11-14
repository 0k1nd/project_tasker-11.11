from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from myapp.models import Task, Comment, Project, Account


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')

    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        data['email'] = self.user.email

        return data


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class ProjectTaskSerializer(ModelSerializer):
    tasks = TaskSerializer(many=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'tasks','editors', 'description']
        annotated_tasks = serializers.IntegerField(read_only=True)

    def get_tasks(self):
        return Task.objects.filter(project=model.id)


class ProjectUserSerializer(ModelSerializer):
    editors = UserSerializer(many=True)

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
        
    def get_comments(self):
        return Comment.objects.filter(comments=model.id)
