import pytest

from rest_framework.test import APIClient

from authentication.models import User
from tests.helpers import assert_api_create

API = '/api/signup/'

valid_payload = {
    "first_name": "jhio",
    "last_name": "dalagan",
    "username": "jhio",
    "password": "jhio",
    "confirm_password": "jhio"
}

@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="jhio",
        password="jhio"
    )

@pytest.mark.django_db
def test_failed_first_name_register(client_for_testing):
    curr_payload = valid_payload.copy()
    curr_payload["first_name"] = "jhi423;,.;'.34o"

    response = assert_api_create(client=client_for_testing, api=API, payload=curr_payload, expected_status=400)
    assert response.data["first_name"][0] == "Name cannot have numbers and symbols aside apostrophe"

@pytest.mark.django_db
def test_failed_last_name_register(client_for_testing):
    curr_payload = valid_payload.copy()
    curr_payload["last_name"] = "dala1234123'.'.gan"

    response = assert_api_create(client=client_for_testing, api=API, payload=curr_payload, expected_status=400)
    assert response.data["last_name"][0] == "Name cannot have numbers and symbols aside apostrophe"

@pytest.mark.django_db
def test_failed_username_register(client_for_testing):
    curr_payload = valid_payload.copy()
    curr_payload["username"] = "jhi;.;'.;'.';o"
    
    response = assert_api_create(client=client_for_testing, api=API, payload=curr_payload, expected_status=400)
    assert "username" in response.data

@pytest.mark.django_db
def test_failed_username_exists_register(client_for_testing, user_for_testing):
    response = assert_api_create(client=client_for_testing, api=API, payload=valid_payload, expected_status=400)

    assert response.status_code == 400
    assert response.data["username"][0] == "Username already taken"

@pytest.mark.django_db
def test_success_register_user(client_for_testing):
    response = assert_api_create(client=client_for_testing, api=API, payload=valid_payload)
    assert "tokens" in response.data
    assert "user" in response.data