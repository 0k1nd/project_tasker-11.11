from django.contrib.messages.views import SuccessMessageMixin
from rest_framework import response
from rest_framework.authtoken.admin import User
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from .serializers import UserSerializer, ProjectTaskSerializer, TaskSerializer, CommentSerializer, ProjectTaskSerializer, TaskCommentSerializer, ProjectSerializer, MemberSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .forms import ProjectForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.decorators import user_passes_test
from myapp.models import Task, Comment, Project, Member
from django.db.models import Count


class RegistrationAPIView(APIView):

  def post(self, request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
      user = serializer.save()
      refresh = RefreshToken.for_user(user)
      return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
      }, status=status.HTTP_201_CREATED)

class TokenObtainPairView(APIView):
  permission_classes = (AllowAny,)
  serializer_class = UserSerializer

  def post(self, request, *args, **kwargs):
    email = request.data.get('email')
    password = request.data.get('password')

    if email and password:
      user = User.objects.filter(email=email).first()
      refresh = RefreshToken.for_user(user)
      return response.Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
      })
    return response.Response({'error': 'Поля email и пароль обязательны!'}, status=status.HTTP_401_UNAUTHORIZED)

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'project', 'created_at', 'assignee']
    search_fields = ['created_at', 'assignee.id']
    ordering_fields = []

    @action(detail=False, url_path="comments")
    def list_comments(self, request):
        queryset = Task.objects.all()
        serializer = TaskCommentSerializer(queryset, many=True)
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated | IsAdminUser])
def create_project(request):
    serializer = ProjectSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all().annotate(
        projects_task = Count('tasks'), projects_user=Count('editors')
    )
    
    @action(detail=False, url_path="tasks_with_annotated")
    def list_tasks_with_annotated(self, request):
        queryset = Project.objects.all()
        serializer = ProjectTaskSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path="tasks")
    def list_tasks(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                queryset = Project.objects.all()
                serializer = ProjectTaskSerializer(queryset, many=True)
                return Response(serializer.data)
            else:
                return HttpResponse("вас нет в этом проекте")
            
@login_required
def edit_project(request, project_id):
    project = Project.objects.get(id=project_id)
    if request.user == project.owner:
        if request.method == 'POST':
            form = ProjectForm(request.POST, instance=project)
            if form.is_valid():
                form.save()
                return redirect('project_detail', project_id=project.id)
        else:
            return redirect('permission_denied')
    else:
        return redirect('permission_denied')

@api_view(['GET'])
@permission_classes([IsAuthenticated | IsAdminUser])
def list_projects(request):
    projects = Project.objects.filter(owner=request.user)
    serializer = ProjectSerializers(projects, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated | IsAdminUser])
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    serializer = ProjectSerializers(project)
    return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated | IsAdminUser])
def update_project(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    serializer = ProjectSerializers(project, data=request.data, partial=True)  # partial=True для PATCH-запроса
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated | IsAdminUser])
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    project.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

class AddMemberView(APIView):
    permission_classes = [IsAuthenticated | IsAdminUser]

    @api_view(['POST'])
    def post(self, request, id):
        project = get_object_or_404(Project, id=id)
        email = request.data.get('email')
        user = get_object_or_404(User, email=email)
        if Member.objects.filter(editable_object=project, user=user).exists():
            return Response({"error": "Пользователь уже участник проекта!"}, status=status.HTTP_400_BAD_REQUEST)
        Member.objects.create(editable_object=project, user=user)
        return Response({"message": "Пользователь успешно добавлен!"}, status=status.HTTP_201_CREATED)

class RemoveMemberView(APIView):
    permission_classes = [IsAuthenticated | IsAdminUser]

    @api_view(['POST'])
    def post(self, request, id):
        project = get_object_or_404(Project, id=id)
        email = request.data.get('email')
        user = get_object_or_404(User, email=email)
        membership = Member.objects.filter(project=project, user=user).first()
        if not membership:
            return Response({"error": "Пользователь уже не участник проекта!"}, status=status.HTTP_400_BAD_REQUEST)
        membership.delete()
        return Response({"message": "Пользователь успешно удален"}, status=status.HTTP_200_OK)

class ListMemberView(APIView):
    permission_classes = [IsAuthenticated | IsAdminUser]

    def get(self, request, id):
        project = get_object_or_404(Project, id=id)

        if not Member.objects.filter(project=project, user=request.user).exists() and project.admin != request.user:
            return Response({"error": "Доступ запрещен"}, status=status.HTTP_403_FORBIDDEN)
        memberships = Member.objects.filter(project=project)
        serializer = MemberSerializer(memberships, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProjectSummaryView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):
        project = get_object_or_404(Project, id=id)
        tasks = project.tasks.all()
        tasks_by_status = tasks.values('status').annotate(count=Count('status'))
        tasks_status_summary = {
            "new": 0,
            "in_progress": 0,
            "done": 0,
        }
        for item in tasks_by_status:
            tasks_status_summary[item['status']] = item['count']

        active_members = project.members.filter(is_active=True)
        active_members_data = MemberSerializer(active_members, many=True).data

        summary_data = {
            'total_tasks': tasks.count(),
            'tasks_by_status': tasks_status_summary,
            'active_members': active_members_data,
        }

        return Response(summary_data, status=status.HTTP_200_OK)

