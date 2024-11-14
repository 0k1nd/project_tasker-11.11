from pickle import FALSE

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import context
from django.utils import timezone
from django.views.generic import CreateView, UpdateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.decorators import user_passes_test
from myapp.serializers import TaskSerializer, CommentSerializer, ProjectTaskSerializer, ProjectUserSerializer, ProjectSerializer, TaskCommentSerializer
from myapp.models import Task, Comment, Project, Account
from django.db.models import Count, Case, When, Avg


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

class OneProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    lookup_field = 'pk'

    @action(detail=False, url_path="tasks")
    def list_projects(self, request, pk):
        model = Project
        print(request.user)
        if request.user.is_authenticated:
            if Account.objects.filter(editable_objects__id=4) or request.user.is_superuser:
                queryset = Project.objects.get(pk=pk)
                serializer = ProjectTaskSerializer(queryset, many=True)
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

