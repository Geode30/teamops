from django.contrib.auth import authenticate
from rest_framework import status, mixins, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import User
from authentication.serializers import LoginSerializer, SignupSerializer, UserSerializer, UpdateCredentialsSerializer
from authentication.services import login_service, logout_service, signup_service, update_credentials_service, token_refresh_service

# Create your views here.

class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        login_serializer = LoginSerializer(data=request.data)
        login_serializer.is_valid(raise_exception=True)
        
        user = login_serializer.validated_data["user"]
        
        access, refresh = login_service(user)
        response = Response({
            "access": access
        }, status=status.HTTP_200_OK)

        response.set_cookie(
            key="refresh",
            value=refresh,
            httponly=True,
            secure=True,
            samesite="None"
        )
        return response

class LogoutView(APIView):
    permission_classes = []

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh")

        if refresh_token:
            logout_service(refresh_token)

        response = Response(
            {"message": "Logged out successfully"},
            status=status.HTTP_200_OK
        )

        return response

class TokenRefreshView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh")

        if not refresh_token:
            return Response(
                {"message": "Refresh token not found in cookies"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        data = token_refresh_service(refresh_token)

        if data["error"]:
            return Response(
                {"message": data["error"]},
                status=status.HTTP_401_UNAUTHORIZED
            )

        response = Response({"access": data["access"]}, status=status.HTTP_200_OK)
        response.set_cookie(
            key="refresh",
            value=data["refresh"],
            httponly=True,
            secure=True,
            samesite="None"
        )
        return response

class SignupView(APIView):
    permission_classes = []

    def post(self, request):
        signup_serializer = SignupSerializer(data=request.data)
        signup_serializer.is_valid(raise_exception=True)

        username = signup_serializer.validated_data['username']
        password = signup_serializer.validated_data['password']
        first_name  = signup_serializer.validated_data['first_name']
        last_name  = signup_serializer.validated_data['last_name']

        data = signup_service(username, password, first_name, last_name)

        return Response({
            "message": "User created successfully",
            **data
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

class CurrentUserView(APIView):
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
        