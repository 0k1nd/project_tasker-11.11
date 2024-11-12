from pickle import FALSE

from django.contrib.auth.mixins import PermissionRequiredMixin
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

# from mysite.myapp.forms import PostForm
from myapp.serializers import TaskSerializer, CommentSerializer, ProjectSerializer, ProjectUserSerializer
from myapp.models import Task, Comment, Project
#from myapp.permissions import IsEditor


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['created_at', 'assignee.id']
    ordering_fields = []
    """permission_classes = [IsEditor]

    def get_queryset(self):
        user = self.request.user
        if not self.request.user.groups.filter(name='editor').exists():
            queryset = queryset.filter(assignee=self.request.user)
            return queryset"""

class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

class ProjectCommentViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    @action(detail=False, url_path="tasks")
    def list_projects(self, request):
        queryset = Project.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path="users")
    def list_users(self, request):
        queryset = Project.objects.all()
        serializer = ProjectUserSerializer(queryset, many=True)
        return Response(serializer.data)
