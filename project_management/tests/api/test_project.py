from rest_framework.test import APIClient

import pytest

from project_management.models import Project

from tests.helpers import assert_api_create, assert_api_update, assert_api_list, assert_api_retrieve, assert_api_delete

API = "/api/project/"

@pytest.mark.django_db
def test_create_project_invalid_deadline(auth_client, user_for_testing):
    payload = {
        "name": "Test project",
        "description": "Test project",
        "status": Project.Status.ACTIVE,
        "priority": Project.Priority.LOW,
        "deadline": "2026-04-30 13:00:00",
        "members": [user_for_testing.id]
    }

    response = assert_api_create(client=auth_client, api=API, payload=payload, expected_status=400)
    assert response.data["deadline"][0] == "Deadline cannot be in the past"

@pytest.mark.django_db
def test_create_project_success(auth_client, user_for_testing):
    payload = {
        "name": "Test project",
        "description": "Test project",
        "status": Project.Status.ACTIVE,
        "priority": Project.Priority.LOW,
        "deadline": "2026-05-30 13:00:00+08:00",
        "members": [user_for_testing.id]
    }

    response = assert_api_create(client=auth_client, api=API, payload=payload)
    project = Project.objects.filter(id=response.data["id"])
    assert project.exists()

@pytest.mark.django_db
def test_get_projects_list(auth_client, projects_for_testing):
    assert_api_list(client=auth_client, api=API, instances=projects_for_testing)

@pytest.mark.django_db
def test_get_specific_project(auth_client, project_for_testing):
    assert_api_retrieve(client=auth_client, api=API, instance=project_for_testing)

@pytest.mark.django_db
def test_update_project_invalid_deadline(auth_client, user_for_testing, project_for_testing):
    payload = {
        "name": "Test project",
        "description": "Test project",
        "status": "active",
        "priority": "low",
        "deadline": "2026-04-30 13:00:00",
        "members": [user_for_testing.id]
    }

    response = assert_api_update(client=auth_client, api=API, instance=project_for_testing, payload=payload, expected_status=400)
    assert response.data["deadline"][0] == "Deadline cannot be in the past"

@pytest.mark.django_db
def test_update_project_success(auth_client, user_for_testing, project_for_testing):
    payload = {
        "name": "Edit Test project",
        "description": "Edit Test project",
        "status": "completed",
        "priority": "high",
        "deadline": "2026-07-30 13:00:00+08:00",
        "members": [user_for_testing.id]
    }

    response = assert_api_update(client=auth_client, api=API, instance=project_for_testing, payload=payload)
    assert response.data["name"] == payload["name"]

@pytest.mark.django_db
def test_delete_project_project_already_deleted(auth_client, progress_note_for_testing_deleted):
    response = assert_api_delete(client=auth_client, api=API, instance=progress_note_for_testing_deleted, expected_status=404)
    assert response.data["detail"] == "No Project matches the given query."

@pytest.mark.django_db
def test_delete_project_success(auth_client, project_for_testing):
    assert_api_delete(client=auth_client, api=API, instance=project_for_testing)
    project = Project.objects.filter(id=project_for_testing.id, date_deleted__isnull=True)
    assert not project.exists()

@pytest.mark.django_db
def test_get_project_id_and_name_list(auth_client, projects_for_testing):
    response = auth_client.get(f"/api/project_id_name/")

    assert response.status_code == 200
    assert isinstance(response.data, list)