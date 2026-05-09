from django.db import models
from authentication.models import TimeStampedModel, User

# Create your models here.

class Project(TimeStampedModel):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        COMPLETED = 'completed', 'Completed'
    
    class Priority(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects_created_by")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.LOW)
    date_completed = models.DateTimeField(blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)

    members = models.ManyToManyField(User, related_name='projects')

    def delete(self, *args, **kwargs):
        self.soft_delete()

class Task(TimeStampedModel):
    class Status(models.TextChoices):
        TODO = 'todo', 'To Do'
        IN_PROGRESS = 'in_progress', 'In Progress'
        DONE = 'done', 'Done'

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks_created_by")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks_project")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.TODO)
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    date_completed = models.DateTimeField(null=True, blank=True)

    def delete(self, *args, **kwargs):
        self.soft_delete()

class ProgressNote(TimeStampedModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="progress_notes_task")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="progress_notes_created_by")
    note = models.TextField()

    def delete(self, *args, **kwargs):
        self.soft_delete()