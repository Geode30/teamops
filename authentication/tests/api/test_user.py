import pytest

from rest_framework.test import APIClient

from tests.helpers import assert_api_create, assert_api_update, assert_api_list, assert_api_retrieve, assert_api_delete

API = "/api/user/"

@pytest.mark.django_db
def test_get_users_list(auth_client, users_for_testing):
    assert_api_list(client=auth_client, api=API, instances=users_for_testing)

@pytest.mark.django_db
def test_get_specific_user(auth_client, user_for_testing):
    assert_api_retrieve(client=auth_client, api=API, instance=user_for_testing)

@pytest.mark.django_db
def test_update_user_invalid_first_name_and_last_name(auth_client,user_for_testing):
    payload = {
        "first_name": "jhon123;;'.;' jhio",
        "last_name": "dalaga;l;3'21n"
    }

    response = assert_api_update(client=auth_client, api=API, instance=user_for_testing, payload=payload, expected_status=400)    
    assert response.data["first_name"][0] == "Name cannot have numbers and symbols aside apostrophe"
    assert response.data["last_name"][0] == "Name cannot have numbers and symbols aside apostrophe"

@pytest.mark.django_db
def test_update_user_success(auth_client, user_for_testing):
    payload = {
        "first_name": "jhon jhio",
        "last_name": "dalagan"
    }
    response = assert_api_update(client=auth_client, api=API, instance=user_for_testing, payload=payload)
    assert response.data["first_name"] == payload["first_name"]
    assert response.data["last_name"] == payload["last_name"]

@pytest.mark.django_db
def test_update_credentials_invalid_username(auth_client, user_for_testing):
    payload = {
        "username": "jhio;.;'.;'.",
        "confirm_password": "jhio",
        "password": "jhio"
    }

    response = auth_client.put(f"/api/update_credentials/{user_for_testing.id}/", payload, format="json")
    assert response.status_code == 400
    assert "username" in response.data

@pytest.mark.django_db
def test_update_credentials_password_mismatch(auth_client, user_for_testing):
    payload = {
        "username": "jhio",
        "confirm_password": "jhio123",
        "password": "jhio"
    }

    response = auth_client.put(f"/api/update_credentials/{user_for_testing.id}/", payload, format="json")
    assert response.status_code == 400
    assert response.data["message"][0] == "Passwords do not match"

@pytest.mark.django_db
def test_update_credentials_success(auth_client, user_for_testing):
    payload = {
        "username": "jhio123",
        "confirm_password": "jhio",
        "password": "jhio"
    }
    response = auth_client.put(f"/api/update_credentials/{user_for_testing.id}/", payload, format="json")
    assert response.status_code == 200
    assert response.data["message"] == "User credentials successfully updated"

@pytest.mark.django_db
def test_get_current_user(auth_client, user_for_testing):
    response = auth_client.get("/api/me/user/")

    assert response.status_code == 200
    assert response.data["id"] == user_for_testing.id
