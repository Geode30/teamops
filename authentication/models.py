from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

from django.utils import timezone

# Create your models here.

class TimeStampedModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def soft_delete(self):
        """Mark the object as deleted without removing it from the database."""
        self.date_deleted = timezone.now()
        self.save()

    def restore(self):
        """Restore a soft-deleted object."""
        self.date_deleted = None
        self.save()

    @property
    def is_deleted(self):
        return self.date_deleted is not None

class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(username=username)
        user.set_password(password)  # hashes password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(username, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, TimeStampedModel):
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin
    
    def delete(self, *args, **kwargs):
        self.soft_delete()