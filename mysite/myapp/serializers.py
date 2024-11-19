from rest_framework.serializers import ModelSerializer
from rest_framework import  serializers
from myapp.models import Task, Comment, Project, Account
from django.db.models import F



class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

class TaskSerializer(ModelSerializer):
    assignee  = AccountSerializer(many=True)
    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'assignee']


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class UserSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = ['username', 'email', 'pined_task']


class ProjectTaskSerializer(ModelSerializer):
    tasks = TaskSerializer(many=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'tasks', 'description']
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
    task_new = serializers.IntegerField(read_only=True)
    task_done = serializers.IntegerField(read_only=True)
    task_in_progress = serializers.IntegerField(read_only=True)
    editors = UserSerializer(many=True)
    tasks = TaskSerializer(many=True)
    # without_assignee = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['name','id','updated_at','projects_task', 'task_new', 'task_done', 'task_in_progress',  'tasks', 'projects_user', 'editors']

    def get_editors(self):
        return Account.objects.filter(editable_objects=model.id)

    def get_tasks(self):
        return Task.objects.filter(project=model.id)

    # def get_without_assignee(self):
    #     return Task.objects.all().order_by(F('assignee').desc(nulls_last=True))
    #


class TaskCommentSerializer(ModelSerializer):
    comments = CommentSerializer(many=True)

    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'comments']

    def get_comments(self):
        return Comment.objects.filter(task=model.id)
