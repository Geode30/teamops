from django.urls import path, include

from rest_framework.routers import DefaultRouter

from project_management.views import ProjectViewSet

router = DefaultRouter()
router.register(r'project', ProjectViewSet, basename='project')

urlpatterns = [
    path('', include(router.urls)),
]