from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.decorators import user_passes_test
from myapp.serializers import TaskSerializer, CommentSerializer, ProjectTaskSerializer, ProjectUserSerializer, ProjectSerializer, TaskCommentSerializer
from myapp.models import Task, Comment, Project, Account
from django.db.models import Count


def user_required():
    def in_groups(user_required):
        if user_required.is_authenticated():
            if Account.objects.filter(project=model.id) | user_required.is_superuser:
                return True
        return False

    return user_passes_test(in_groups)


#from myapp.permissions import IsEditor


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['created_at', 'assignee.id']
    ordering_fields = []

    @action(detail=False, url_path="comments")
    def list_comments(self, request):
        queryset = Task.objects.all()
        serializer = TaskCommentSerializer(queryset, many=True)
        return Response(serializer.data)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all().annotate(
        projects_task = Count('tasks'), projects_user=Count('editors')
    )

    @action(detail=False, url_path="tasks")
    def list_projects(self, request, pk):
        project = Project.objects.get(pk=pk)
        if request.user.is_authenticated:
            if request.user.is_superuser:
                tasks = Task.objects.filter(project=project)
                serializer = TaskSerializer(tasks, many=True)
                return Response(serializer.data)
            else:
                return HttpResponse("вас нет в этом проекте")
        else:
            return HttpResponse("Пожалуйста, авторизуйтесь.")


    @action(detail=False, url_path="users")
    def list_users(self, request, pk):
        queryset = Project.objects.filters(pk=pk)
        serializer = ProjectUserSerializer(queryset, many=True)
        return Response(serializer.data)

