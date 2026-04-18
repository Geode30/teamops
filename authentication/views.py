from django.contrib.auth import authenticate
from rest_framework import status, mixins, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import User
from authentication.serializers import LoginSerializer, SignupSerializer, UserSerializer, UpdateCredentialsSerializer
from authentication.services import login_service, signup_service, update_credentials_service

# Create your views here.

class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        login_serializer = LoginSerializer(data=request.data)
        login_serializer.is_valid(raise_exception=True)
        
        user = login_serializer.validated_data["user"]
        
        access, refresh = login_service(user)

        return Response({
            "access": access,
            "refresh": refresh
        }, status=status.HTTP_200_OK)

class SignupView(APIView):
    permission_classes = []

    def post(self, request):
        signup_serializer = SignupSerializer(data=request.data)
        signup_serializer.is_valid(raise_exception=True)

        username = signup_serializer.validated_data['username']
        password = signup_serializer.validated_data['password']

        data = signup_service(username, password)

        return Response({
            "message": "User created successfully",
            "user": {
                "id": data['user_id'],
                "username": data['username']
            },
            "tokens": data['tokens']
        }, status=status.HTTP_201_CREATED)

class UpdateCredentialsView(APIView):
    def put(self, request, id):
        data = request.data
        data['user'] = id
        update_credentials_serializer = UpdateCredentialsSerializer(data=data)
        update_credentials_serializer.is_valid(raise_exception=True)

        user = update_credentials_serializer.validated_data['user']
        username = update_credentials_serializer.validated_data['username']
        password = update_credentials_serializer.validated_data['password']

        update_credentials_service(user, username, password)

        return Response({
            "message": "User credentials successfully updated"
        }, status=status.HTTP_200_OK)

class UserViewSet(
    mixins.RetrieveModelMixin, 
    mixins.ListModelMixin, 
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin, 
    viewsets.GenericViewSet
):
    queryset = User.objects.filter(date_deleted__isnull=True)
    serializer_class = UserSerializer
        