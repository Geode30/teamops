import pytest

from project_management.models import ProgressNote
from tests.helpers import assert_api_create, assert_api_update, assert_api_list, assert_api_retrieve, assert_api_delete

API = "/api/progress_note/"

@pytest.mark.django_db
def test_create_progress_note_success(auth_client, task_for_testing):
    payload = {
        "task": task_for_testing.id,
        "note": "Test progress note"
    }

    response = assert_api_create(client=auth_client, api=API, payload=payload)
    assert ProgressNote.objects.filter(id=response.data["id"]).exists()
    assert response.data["note"] == payload["note"]

@pytest.mark.django_db
def test_create_progress_note_project_completed(auth_client, task_for_testing_project_completed):
    payload = {
        "task": task_for_testing_project_completed.id,
        "note": "Test progress note"
    }
    
    response = assert_api_create(client=auth_client, api=API, payload=payload, expected_status=400)
    assert response.data["message"][0] == "Cannot add a note to a completed project"

@pytest.mark.django_db
def test_update_progress_note_success(auth_client, task_for_testing, progress_note_for_testing):
    payload = {
        "task": task_for_testing.id,
        "note": "Test progress note updated"
    }

    response = assert_api_update(client=auth_client, api=API, instance=progress_note_for_testing, payload=payload)
    assert response.data["id"] == progress_note_for_testing.id
    assert response.data["note"] == payload["note"]

@pytest.mark.django_db
def test_update_progress_project_completed(auth_client, task_for_testing_project_completed, progress_note_for_testing):
    payload = {
        "task": task_for_testing_project_completed.id,
        "note": "Test progress note updated"
    }

    response = assert_api_update(client=auth_client, api=API, instance=progress_note_for_testing, payload=payload, expected_status=400)
    assert response.data["message"][0] == "Cannot add a note to a completed project"

@pytest.mark.django_db
def test_get_progress_notes_list(auth_client, progress_notes_for_testing):
    assert_api_list(client=auth_client, api=API, instances=progress_notes_for_testing)

@pytest.mark.django_db
def test_get_specific_progress_note(auth_client, progress_note_for_testing):
    assert_api_retrieve(client=auth_client, api=API, instance=progress_note_for_testing)

@pytest.mark.django_db
def test_delete_progress_note_success(auth_client, progress_note_for_testing):
    assert_api_delete(client=auth_client, api=API, instance=progress_note_for_testing)
    progress_note = ProgressNote.objects.filter(id=progress_note_for_testing.id, date_deleted__isnull=True)
    assert not progress_note.exists()

@pytest.mark.django_db
def test_delete_progress_note_not_exists(auth_client, progress_note_for_testing_deleted):
    response = assert_api_delete(client=auth_client, api=API, instance=progress_note_for_testing_deleted, expected_status=404)
    assert response.data["detail"] == "No ProgressNote matches the given query."