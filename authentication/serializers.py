from django.contrib.auth import authenticate

from rest_framework import serializers

from authentication.models import User
from authentication.utils import validate_username

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError({
                "message": "Invalid credentials"
            })
        
        data['user'] = user
        
        return data

class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    password = serializers.CharField(write_only=True)

    def validate_username(self, value):
        return validate_username(value)

class UpdateCredentialsSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(date_deleted__isnull=True))
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True)

    def validate_username(self, value):
        return validate_username(value, is_update=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']
        read_only_fields = ['username']