from rest_framework.test import APIClient

import pytest

from project_management.models import Task
from tests.helpers import assert_api_create, assert_api_update, assert_api_list, assert_api_retrieve, assert_api_delete, api_request

API = "/api/task/"

@pytest.mark.django_db
def test_create_task_success(auth_client, project_for_testing):
    payload = {
        "project": project_for_testing.id,
        "name": "Test task",
        "description": "Test task",
        "status": Task.Status.TODO,
        "assigned_to": None
    }

    response = assert_api_create(client=auth_client, api=API, payload=payload)
    task = Task.objects.filter(id=response.data["id"])
    assert task.exists()

@pytest.mark.django_db
def test_create_task_completed_project(auth_client, project_for_testing_completed):
    payload = {
        "project": project_for_testing_completed.id,
        "name": "Test task",
        "description": "Test task",
        "status": Task.Status.TODO,
        "assigned_to": None
    }

    response = assert_api_create(client=auth_client, api=API, payload=payload, expected_status=400)
    assert response.data["message"][0] == "Cannot assign task to a completed project"

@pytest.mark.django_db
def test_update_task_success(auth_client, user_for_testing, task_for_testing, project_for_testing):
    payload = {
        "project": project_for_testing.id,
        "name": "Test task Update",
        "description": "Test task Update",
        "status": Task.Status.IN_PROGRESS,
        "assigned_to": user_for_testing.id
    }

    response = assert_api_update(client=auth_client, api=API, instance=task_for_testing, payload=payload)
    assert response.data["name"] == payload["name"]

@pytest.mark.django_db
def test_update_task_completed_project(auth_client, user_for_testing, task_for_testing, project_for_testing_completed):
    payload = {
        "project": project_for_testing_completed.id,
        "name": "Test task Update",
        "description": "Test task Update",
        "status": Task.Status.IN_PROGRESS,
        "assigned_to": user_for_testing.id
    }

    response = assert_api_update(client=auth_client, api=API, instance=task_for_testing, payload=payload, expected_status=400)
    assert response.data["message"][0] == "Cannot assign task to a completed project"

@pytest.mark.django_db
def test_get_tasks_list(auth_client, tasks_for_testing):
    assert_api_list(client=auth_client, api=API, instances=tasks_for_testing)

@pytest.mark.django_db
def test_get_tasks_list_filtered_by_project(auth_client, project_for_testing, tasks_for_testing):
    response = api_request(
        client=auth_client,
        method="get",
        url=API,
        expected_status=200,
        query_params={"project": project_for_testing.id} 
    )
    
    assert isinstance(response.data, list)
    assert len(response.data) != 0
    assert all(
        task["project"] == project_for_testing.id
        for task in response.data
    )

@pytest.mark.django_db
def test_get_specific_task(auth_client, task_for_testing):
    assert_api_retrieve(client=auth_client, api=API, instance=task_for_testing)

@pytest.mark.django_db
def test_delete_task_success(auth_client, task_for_testing):
    assert_api_delete(client=auth_client, api=API, instance=task_for_testing)
    task = Task.objects.filter(id=task_for_testing.id, date_deleted__isnull=True)
    assert not task.exists()

@pytest.mark.django_db
def test_delete_task_not_exists(auth_client, task_for_testing_deleted):
    response = assert_api_delete(client=auth_client, api=API, instance=task_for_testing_deleted, expected_status=404)
    assert response.data["detail"] == "No Task matches the given query."
