from rest_framework_simplejwt.tokens import RefreshToken
from authentication.models import User

def login_service(user):    
    refresh = RefreshToken.for_user(user)

    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    return access_token, refresh_token

def signup_service(username, password, first_name, last_name):
    first_name = first_name.title()
    last_name = last_name.title()

    user = User(first_name=first_name, last_name=last_name, username=username)
    user.set_password(password)
    user.save()

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