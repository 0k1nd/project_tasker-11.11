from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Count
from myapp.models import Task, Comment, Project, Account
from myapp.serializers import TaskSerializer, CommentSerializer, ProjectTaskSerializer, ProjectUserSerializer, ProjectSerializer, TaskCommentSerializer

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
def task_actions(request, pk):
    if request.method == 'GET':
        queryset = Task.objects.filter(pk=pk)
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
        queryset = Task.objects.filter(pk=pk)
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

