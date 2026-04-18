from django.urls import path, include

from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import TokenRefreshView

from authentication.views import LoginView, SignupView, UserViewSet, UpdateCredentialsView

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='item')

urlpatterns = [
    path('', include(router.urls)),

    path('login/', LoginView.as_view()),
    path('signup/', SignupView.as_view()),
    path('update_credentials/<int:id>/', UpdateCredentialsView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]