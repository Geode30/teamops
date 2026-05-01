from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.models import User
from django.contrib.auth.models import update_last_login

def login_service(user):    
    update_last_login(None, user)
    refresh = RefreshToken.for_user(user)

    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    return access_token, refresh_token

def logout_service(refresh_token):
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
    except Exception:
        pass  # token might already be invalid

    return None

def signup_service(username, password, first_name, last_name):
    first_name = first_name.title()
    last_name = last_name.title()

    user = User(first_name=first_name, last_name=last_name, username=username)
    user.set_password(password)
    user.save()

    update_last_login(None, user)

    refresh = RefreshToken.for_user(user)

    return {
        "user": {
            "user_id": user.id,
            "username": user.username,
            "first_name": first_name,
            "last_name": last_name,
        },
        "tokens": {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
    }

def update_credentials_service(user: User, username, password):
    user.username = username
    user.set_password(password)
    user.save()

def token_refresh_service(refresh_token):
    try:
        # Validate refresh token
        token = RefreshToken(refresh_token)
        user_id = token["user_id"]
        user = User.objects.get(id=user_id)

        token.blacklist()

        # Create new tokens
        new_refresh = RefreshToken.for_user(user)

        access_token = str(new_refresh.access_token)
        refresh_token_str = str(new_refresh)

        return {
            "access": access_token,
            "refresh": refresh_token_str,
            "error": False
        }

    except TokenError:
        return {
            "error": "Invalid or expired refresh token"
        }