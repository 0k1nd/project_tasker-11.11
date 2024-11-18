from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Count
from myapp.models import Task, Comment, Project, Account
import django_filters.rest_framework
from django.http import JsonResponse
from myapp.serializers import TaskSerializer, CommentSerializer, ProjectTaskSerializer, ProjectUserSerializer, ProjectSerializer, TaskCommentSerializer, UserSerializer

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

@api_view(['GET'])
def filter_tasks(request, pk):
    status = request.GET.get('status')
    assignee = request.GET.get('assignee')
    created_at = request.GET.get('created_at__gte')
    queryset = Task.objects.filter(project=pk)
    if status:
        queryset = queryset.filter(status=status)
    if assignee:
        queryset = queryset.filter(assignee=assignee)
    if created_at:
        queryset = queryset.filter(created_at__gte=created_at)
    tasks = list(queryset.values())
    return JsonResponse(tasks, safe=False)

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
        queryset = Account.objects.filter(pined_task=pk)
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
def tasks_report(request, pk):
    queryset = Project.objects.filter(pk=pk).annotate(
        task_in_progress=Count(Task.objects.filter(status=in_progress)), task_done=Count(Task.objects.filter(status=done)), task_new=Count(Task.objects.filter(status=new)),withoutass=(Task.objects.filter(assignee__isnull=True)), projects_task = Count('tasks')
    )
    serializer = ProjectSerializer(queryset, many=True)
    return Response(serializer.data)
                               
        