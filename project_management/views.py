from django.db.models import Q

from rest_framework import status, mixins, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from project_management.models import Project, Task, ProgressNote
from project_management.serializers import ProjectSerializer, ProjectIDandNameSerializer, TaskSerializer, ProgressNoteSerializer

# Create your views here.

class ProjectViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin, 
    mixins.ListModelMixin, 
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin, 
    viewsets.GenericViewSet
):
    queryset = Project.objects.filter(date_deleted__isnull=True).select_related('created_by')
    serializer_class = ProjectSerializer

class ProjectIDandNameView(APIView):
    def get(self, request):
        user = request.user
        user_filter = Q(created_by=user) | Q(members=user)
        projects = Project.objects.only('id', 'name').filter(user_filter, date_deleted__isnull=True).distinct()
        if projects.exists():
            serializer = ProjectIDandNameSerializer(projects, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response([], status=status.HTTP_200_OK)

class TaskViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin, 
    mixins.ListModelMixin, 
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin, 
    viewsets.GenericViewSet             
):
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.filter(date_deleted__isnull=True).select_related('assigned_to')
        project = self.request.query_params.get('project')

        if project:
            queryset = queryset.filter(project=project)

        return queryset

class ProgressNoteViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin, 
    mixins.ListModelMixin, 
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin, 
    viewsets.GenericViewSet
):
    queryset = ProgressNote.objects.filter(date_deleted__isnull=True)
    serializer_class = ProgressNoteSerializer