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
    task_now = serializers.IntegerField(read_only=True)
    task_done = serializers.IntegerField(read_only=True)
    task_in_progress = serializers.IntegerField(read_only=True)
    project_tasks = serializers.IntegerField(read_only=True)
    without_ass = serializers.IntegerField(read_only=True)
    editors = UserSerializer(many=True)
    tasks = TaskSerializer(many=True)
    
    class Meta:
        model = Project
        fields = '__all__'

    def get_editors(self):
        return Account.objects.filter(editable_objects=model.id)

    def get_tasks(self):
        return Task.objects.filter(project=model.id)
        

class TaskCommentSerializer(ModelSerializer):
    comments = CommentSerializer(many=True)

    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'comments']

    def get_comments(self):
        return Comment.objects.filter(task=model.id)
