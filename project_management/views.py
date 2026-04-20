from rest_framework import status, mixins, viewsets

from project_management.models import Project
from project_management.serializers import ProjectSerializer

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