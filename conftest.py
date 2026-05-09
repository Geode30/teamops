import pytest
import random
import string

from rest_framework.test import APIClient

from authentication.models import User
from project_management.models import Project, Task, ProgressNote

def random_string(length=6):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

@pytest.fixture
def client_for_testing():
    return APIClient()

@pytest.fixture
def user_for_testing(db):
    user = User.objects.create_user(
        username="jhio",
        password="jhio"
    )

    user.first_name = "jhio"
    user.last_name = "dalagan"
    user.save()

    return user

@pytest.fixture
def users_for_testing(db):
    users = []

    for _ in range(5):
        username = f"user_{random_string()}"
        first_name = random_string()
        last_name = random_string()

        user = User.objects.create_user(
            username=username,
            password="testpass123"
        )

        user.first_name = first_name
        user.last_name = last_name
        user.save()

        users.append(user)

    return users

@pytest.fixture
def auth_client(client_for_testing, user_for_testing):
    client_for_testing.force_authenticate(user=user_for_testing)
    return client_for_testing

@pytest.fixture
def project_for_testing(db, user_for_testing):
    project = Project.objects.create(
        name="Test project active",
        description="Test project active",
        status=Project.Status.ACTIVE,
        priority=Project.Priority.LOW,
        deadline="2026-06-30 13:00:00+08:00",
        created_by=user_for_testing
    )

    return project

@pytest.fixture
def project_for_testing_deleted(db, user_for_testing):
    project = Project.objects.create(
        name="Test project active",
        description="Test project active",
        status=Project.Status.ACTIVE,
        priority=Project.Priority.LOW,
        deadline="2026-06-30 13:00:00+08:00",
        created_by=user_for_testing,
        date_deleted="2026-04-27 13:00:00+08:00"
    )

    return project

@pytest.fixture
def projects_for_testing(db, user_for_testing):
    projects = [
            Project.objects.create(
            name=f"Test project {i}",
            description="Test project",
            status=Project.Status.ACTIVE,
            priority=Project.Priority.LOW,
            deadline="2026-06-30 13:00:00+08:00",
            created_by=user_for_testing
        )
        for i in range(5)
    ]

    return projects

@pytest.fixture
def project_for_testing_completed(db, user_for_testing):
    project = Project.objects.create(
        name="Test project active",
        description="Test project active",
        status=Project.Status.COMPLETED,
        priority=Project.Priority.LOW,
        deadline="2026-06-30 13:00:00+08:00",
        created_by=user_for_testing,
        date_completed="2026-06-27 13:00:00+08:00"
    )

    return project

@pytest.fixture
def task_for_testing(db, user_for_testing, project_for_testing):
    task = Task.objects.create(
        project=project_for_testing,
        name="Test task",
        description="Test task",
        status=Task.Status.TODO,
        assigned_to=None,
        created_by=user_for_testing
    )

    return task

@pytest.fixture
def task_for_testing_deleted(db, user_for_testing, project_for_testing):
    task = Task.objects.create(
        project=project_for_testing,
        name="Test task",
        description="Test task",
        status=Task.Status.TODO,
        assigned_to=None,
        created_by=user_for_testing,
        date_deleted="2026-04-27 13:00:00+08:00"
    )

    return task

@pytest.fixture
def task_for_testing_project_completed(db, user_for_testing, project_for_testing_completed):
    task = Task.objects.create(
        project=project_for_testing_completed,
        name="Test task",
        description="Test task",
        status=Task.Status.TODO,
        assigned_to=None,
        created_by=user_for_testing
    )

    return task

@pytest.fixture
def tasks_for_testing(db, user_for_testing, project_for_testing):
    tasks = [
            Task.objects.create(
            project=project_for_testing,
            name=f"Test task {i}",
            description="Test task",
            status=Task.Status.TODO,
            assigned_to=None,
            created_by=user_for_testing
        )
        for i in range(5)
    ]

    return tasks

@pytest.fixture
def progress_note_for_testing(db, user_for_testing, task_for_testing):
    progress_note = ProgressNote.objects.create(
        task=task_for_testing,
        note="Test progress note",
        created_by=user_for_testing
    )

    return progress_note

@pytest.fixture
def progress_note_for_testing_deleted(db, user_for_testing, task_for_testing):
    progress_note = ProgressNote.objects.create(
        task=task_for_testing,
        note="Test progress note",
        created_by=user_for_testing,
        date_deleted="2026-04-27 13:00:00+08:00"
    )

    return progress_note

@pytest.fixture
def progress_notes_for_testing(db, user_for_testing, task_for_testing):
    progress_notes = [
        ProgressNote.objects.create(
            task=task_for_testing,
            note=f"Test progress note {i}",
            created_by=user_for_testing
        )
        for i in range(1, 6)
    ]

    return progress_notes
