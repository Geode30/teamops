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
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.choices)
    date_completed = models.DateTimeField(blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)

    members = models.ManyToManyField(User, related_name='projects')

    def delete(self, *args, **kwargs):
        self.soft_delete()