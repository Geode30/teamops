import pytest
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient

from authentication.models import User

def is_token_blacklisted(token_str):
    try:
        RefreshToken(token_str)
        return False
    except TokenError:
        return True

@pytest.mark.django_db
def test_login_user_failed_user_not_exists(client_for_testing):
    login_payload = {
        "username": "jhio",
        "password": "jhio"
    }

    response = client_for_testing.post("/api/login/", login_payload)

    assert response.status_code == 400
    assert "message" in response.data
    assert response.data["message"][0] == "Invalid credentials"

@pytest.mark.django_db
def test_login_user_failed_username_not_exists(client_for_testing, user_for_testing):
    login_payload = {
        "username": "jhio123",
        "password": "jhio"
    }

    response = client_for_testing.post("/api/login/", login_payload)

    assert response.status_code == 400
    assert "message" in response.data
    assert response.data["message"][0] == "Invalid credentials"

@pytest.mark.django_db
def test_login_user_failed_password_incorrect(client_for_testing, user_for_testing):
    login_payload = {
        "username": "jhio",
        "password": "jhio123"
    }

    response = client_for_testing.post("/api/login/", login_payload)

    assert response.status_code == 400
    assert "message" in response.data
    assert response.data["message"][0] == "Invalid credentials"

@pytest.mark.django_db
def test_success_login_user(client_for_testing, user_for_testing):
    login_payload = {
        "username": "jhio",
        "password": "jhio"
    }

    response = client_for_testing.post("/api/login/", login_payload)

    assert response.status_code == 200
    assert "access" in response.data

@pytest.mark.django_db
def test_logout_user(client_for_testing, user_for_testing):
    login_payload = {
        "username": "jhio",
        "password": "jhio"
    }

    # Login
    response = client_for_testing.post("/api/login/", login_payload)
    assert response.status_code == 200
    assert "refresh" in response.cookies

    refresh = response.cookies["refresh"].value

    # Logout
    response = client_for_testing.post("/api/logout/")

    # Check response
    assert response.status_code == 200

    # Check cookie is cleared
    assert "refresh" in response.cookies
    assert response.cookies["refresh"].value == ""

    # Check token is blacklisted
    assert is_token_blacklisted(refresh)

@pytest.mark.django_db
def test_refresh_token(client_for_testing, user_for_testing):
    login_payload = {
        "username": "jhio",
        "password": "jhio"
    }

    # Login
    response = client_for_testing.post("/api/login/", login_payload)
    assert response.status_code == 200
    assert "refresh" in response.cookies

    # Refresh
    response = client_for_testing.post('/api/token/refresh/')

    # Check response
    assert response.status_code == 200
    assert "refresh" in response.cookies
    assert "access" in response.data