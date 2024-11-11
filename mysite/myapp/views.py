from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import CreateView, UpdateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet

# from mysite.myapp.forms import PostForm
from myapp.serializers import TaskSerializer, CommentSerializer
from myapp.models import Task, Comment
from myapp.permitions import IsEditor


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['created_at', 'assignee.id']
    # ordering_fields = ['price', 'author_name']
    permission_classes = [IsEditor]

    def get_queryset(self):
        user = self.request.user
        if not self.request.user.groups.filter(name='editor').exists():
            queryset = queryset.filter(assignee=self.request.user)
            return queryset

class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

"""def task_edit(request, pk):
    post = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})"""