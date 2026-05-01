from django.urls import path, include

from rest_framework.routers import DefaultRouter

from authentication.views import LoginView, LogoutView, SignupView, UserViewSet, UpdateCredentialsView, TokenRefreshView, CurrentUserView

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),

    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('signup/', SignupView.as_view()),
    path('me/user/', CurrentUserView.as_view()),
    path('update_credentials/<int:id>/', UpdateCredentialsView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]