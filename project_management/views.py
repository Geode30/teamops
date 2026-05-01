from django.db.models import Q

from rest_framework import status, mixins, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from project_management.models import Project
from project_management.serializers import ProjectSerializer, ProjectIDandNameSerializer

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
        projects = Project.objects.filter(user_filter, date_deleted__isnull=True).distinct()
        if projects.exists():
            serializer = ProjectIDandNameSerializer(projects, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response([], status=status.HTTP_200_OK)