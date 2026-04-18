from django.contrib.auth import authenticate
from rest_framework import serializers
from authentication.models import User

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
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