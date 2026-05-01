from django.urls import path, include

from rest_framework.routers import DefaultRouter

from project_management.views import ProjectViewSet, ProjectIDandNameView

router = DefaultRouter()
router.register(r'project', ProjectViewSet, basename='project')

urlpatterns = [
    path('', include(router.urls)),

    path('project_id_name/', ProjectIDandNameView.as_view())
]