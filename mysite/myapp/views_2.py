from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Count, Case, When
from myapp.models import Task, Comment, Project, Member
import django_filters.rest_framework
from django.http import JsonResponse

from rest_framework import status
from myapp.serializers import TaskSerializer, CommentSerializer, ProjectTaskSerializer, ProjectSerializer, TaskCommentSerializer, UserSerializer

@api_view()
def project_detail(request, pk):
    queryset = Project.objects.filter(pk=pk).annotate(
        projects_task = Count('tasks'), projects_user=Count('editors')
    )
    serializer = ProjectSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def project_task(request, pk):
    if request.method == 'GET':
        queryset = Project.objects.filter(pk=pk)
        serializer = ProjectTaskSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project=pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH', 'DELETE'])
def task_actions(request, pk,):
    if request.method == 'GET':
        queryset = Task.objects.filter(project=pk)
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        task.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PATCH'])
def change_status(request, pk):
    if request.method == 'GET':
        queryset = Task.status.filter(pk=pk)
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH'])
def change_assign(request, pk):
    if request.method == 'GET':
        queryset = Member.objects.filter(pined_task=pk)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'POST'])
def task_comments(request, pk):
    if request.method == 'GET':
        queryset = Task.objects.filter(pk=pk)
        serializer = TaskCommentSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TaskCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def tasks_report(request):
    projects = Project.objects.all().annotate(
        projects_task = Count('tasks'))
    response = []
    for project in projects:
        progress_serializers = ProjectSerializer(project)
        tasks_new = Task.objects.filter(status="new", project=project.pk)
        new_serializers = TaskSerializer(tasks_new, many=True)
        tasks_done = Task.objects.filter(status="done", project=project.pk)
        done_serializers = TaskSerializer(tasks_done, many=True)
        tasks_in_progress = Task.objects.filter(status="in_progress", project=project.pk)
        in_progress_serializers = TaskSerializer(tasks_in_progress, many=True)
        task_without_assignee = Task.objects.filter(assignee__isnull=True, project=project.pk)
        task_without_assignee_serializers = TaskSerializer(task_without_assignee, many=True)
        response.append({
            "project": progress_serializers.data,
            "new": new_serializers.data,
            "done": done_serializers.data,
            "in_progress": in_progress_serializers.data,
            "without_assignee": task_without_assignee_serializers.data
        })
    return Response(response)


@api_view(['GET'])
def filter_tasks(request, pk):
    queryset = Task.objects.filter(project=pk)
    status_parm = request.GET.get('status')
    assignee_parm = request.GET.get('assignee')
    created_at_parm = request.GET.get('created_at__gte')
    if status:
        queryset = queryset.filter(status=status_parm)
    if assignee:
        queryset = queryset.filter(assignee=assignee_parm)
    if created_at:
        queryset = queryset.filter(created_at__gte=created_at_parm)
    if not queryset.exists():
        return Response({
            "massage": "no task found"
        }, status=status.HTTP_204_NO_CONTENT)
    tasks_serializer = TaskSerializer(queryset, many=True)
    return Response(tasks_serializer)
                               
        