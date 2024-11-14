from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from rest_framework import response
from rest_framework.authtoken.admin import User
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserSerializer, ProjectTaskSerializer, TaskSerializer, CommentSerializer, ProjectTaskSerializer, ProjectUserSerializer, TaskCommentSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .forms import UserForgotPasswordForm, UserSetNewPasswordForm, ProjectForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProjectForm, ParticipantForm
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.decorators import user_passes_test
from myapp.models import Task, Comment, Project, Member, ProjectAdmin
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

class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):
  form_class = UserForgotPasswordForm
  template_name = 'system/user_password_reset.html'
  success_url = reverse_lazy('home')
  success_message = 'Письмо с инструкцией по восстановлению пароля отправлена на ваш email'
  subject_template_name = 'system/email/password_subject_reset_mail.txt'
  email_template_name = 'system/email/password_reset_mail.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = 'Запрос на восстановление пароля'
    return context

class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
  form_class = UserSetNewPasswordForm
  template_name = 'system/user_password_set_new.html'
  success_url = reverse_lazy('home')
  success_message = 'Пароль успешно изменен. Можете авторизоваться на сайте.'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = 'Установить новый пароль'
    return context

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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_project(request):
    serializer = ProjectSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
@permission_classes([IsAuthenticated])
def list_projects(request):
    projects = Project.objects.filter(owner=request.user)
    serializer = ProjectSerializers(projects, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    serializer = ProjectSerializers(project)
    return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_project(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    serializer = ProjectSerializers(project, data=request.data, partial=True)  # partial=True для PATCH-запроса
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    project.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

class AddMemberView(APIView):
    permission_classes = [IsAuthenticated, IsProjectAdmin]

    @api_view(['POST'])
    def post(self, request, id):
        project = get_object_or_404(Project, id=id)
        email = request.data.get('email')
        user = get_object_or_404(User, email=email)
        if Member.objects.filter(project=project, user=user).exists():
            return Response({"error": "Пользователь уже участник проекта!"}, status=status.HTTP_400_BAD_REQUEST)
        Member.objects.create(project=project, user=user)
        return Response({"message": "Пользователь успешно добавлен!"}, status=status.HTTP_201_CREATED)

class RemoveMemberView(APIView):
    permission_classes = [IsAuthenticated, IsProjectAdmin]

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
    permission_classes = [IsAuthenticated]

    @api_view(['GET'])
    def get(self, request, id):
        project = get_object_or_404(Project, id=id)
        if not Member.objects.filter(project=project, user=request.user).exists() and project.admin != request.user:
            return Response({"error": "Доступ запрещен"}, status=status.HTTP_403_FORBIDDEN)
        memberships = Member.objects.filter(project=project)
        serializer = Member(memberships, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProjectSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    @api_view(['GET'])
    def get(self, request, id):
        project = get_object_or_404(Project, id=id)
        if not Member.objects.filter(project=project, user=request.user).exists() and project.owner != request.user:
            return Response({"error": "Доступ запрещен"}, status=403)
        total_tasks = project.tasks.count()
        tasks_by_status = {
            'new': project.tasks.filter(status='new').count(),
            'in_progress': project.tasks.filter(status='in_progress').count(),
            'done': project.tasks.filter(status='done').count(),
        }
        active_members = User.objects.filter(memberships__project=project).distinct()
        summary_data = {
            'total_tasks': total_tasks,
            'tasks_by_status': tasks_by_status,
            'active_members': UserSerializer(active_members, many=True).data,
        }

        serializer = ProjectSummarySerializer(summary_data)
        return Response(serializer.data, status=200)

class OneProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    lookup_field = 'pk'

    @action(detail=False, url_path="tasks")
    def list_projects(self, request, pk):
        model = Project
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

