from authentication.models import User

from rest_framework import serializers

import re

USERNAME_PATTERN = r"[A-Za-z0-9_]+"
PERSON_NAME_PATTERN = r"^[A-Za-z]+(?:[' ][A-Za-z]+)*$"

def validate_username(value, is_update=False):
    if not is_update:
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already taken")

    if not re.fullmatch(USERNAME_PATTERN, value):
        raise serializers.ValidationError(
            "Username cannot have spaces and symbols aside underscore"
        )

    if "__" in value:
        raise serializers.ValidationError(
            "Username cannot have consecutive underscores"
        )

    if value.startswith("_") or value.endswith("_"):
        raise serializers.ValidationError(
            "Username cannot start or end with underscore"
        )

    return value

def is_valid_person_name(name):
    if not re.fullmatch(PERSON_NAME_PATTERN, name):
        raise serializers.ValidationError(
            "Name cannot have numbers and symbols aside apostrophe"
        )
    
    return name
    