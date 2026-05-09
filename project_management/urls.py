from django.urls import path, include

from rest_framework.routers import DefaultRouter

from project_management.views import ProjectViewSet, ProjectIDandNameView, TaskViewSet, ProgressNoteViewSet

router = DefaultRouter()
router.register(r'project', ProjectViewSet, basename='project')
router.register(r'task', TaskViewSet, basename='task')
router.register(r'progress_note', ProgressNoteViewSet, basename='progress_note')

urlpatterns = [
    path('', include(router.urls)),

    path('project_id_name/', ProjectIDandNameView.as_view())
]