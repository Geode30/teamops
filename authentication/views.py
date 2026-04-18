from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response

from authentication.serializers import LoginSerializer
from authentication.services import login_service

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
        })

        