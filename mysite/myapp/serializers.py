from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from myapp.models import Task, Comment, Project, Member
from rest_framework import  serializers
from django.db.models import F

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class MemberSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Member
        fields = ['id','user', 'role']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')

    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        data['email'] = self.user.email

        return data

class TaskSerializer(ModelSerializer):
    assignee  = MemberSerializer(many=True)
    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'assignee']

class ProjectSerializer(ModelSerializer):
    projects_task = serializers.IntegerField(read_only=True)
    projects_user = serializers.IntegerField(read_only=True)
    task_new = serializers.IntegerField(read_only=True)
    task_done = serializers.IntegerField(read_only=True)
    task_in_progress = serializers.IntegerField(read_only=True)
    editors = MemberSerializer(many=True)
    tasks = TaskSerializer(many=True)

    class Meta:
        model = Project
        fields = ['name', 'id', 'updated_at', 'projects_task', 'task_new', 'task_done', 'task_in_progress', 'tasks',
                  'projects_user', 'editors']

    def get_editors(self):
        return Member.objects.filter(editable_objects=model.id)

    def get_tasks(self):
        return Task.objects.filter(project=model.id)


class ProjectSummarySerializer(serializers.Serializer):
    total_tasks = serializers.IntegerField()
    tasks_by_status = serializers.DictField(child=serializers.IntegerField())
    active_members = UserSerializer(many=True)

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class ProjectTaskSerializer(ModelSerializer):
    tasks = TaskSerializer(many=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'tasks', 'description']
        annotated_tasks = serializers.IntegerField(read_only=True)

    def get_tasks(self):
        return Task.objects.filter(project=model.id)



class TaskCommentSerializer(ModelSerializer):
    comments = CommentSerializer(many=True)
    class Meta:
        model = Task
        fields = '__all__'
        
    def get_comments(self):
        return Comment.objects.filter(task=model.id)

