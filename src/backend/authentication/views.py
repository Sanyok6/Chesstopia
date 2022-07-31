from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from rest_framework import permissions, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from . import serializers


class LoginView(views.APIView):
    """View to authenticate user and log them in."""

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        """Handle the login request."""
        login_serializer = serializers.LoginSerializer(data=request.data)
        login_serializer.is_valid(raise_exception=True)

        user = authenticate(request, **login_serializer.data)

        if user is None:
            return Response({'detail': 'Account with the given credentials does not exist'},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        if not user.is_active:
            return Response({'detail': 'User is not active'}, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.set_cookie('isLoggedIn', 'yes', max_age=settings.SESSION_COOKIE_AGE, samesite='Lax')

        return response


class SignupView(views.APIView):
    """View to create a new user."""

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        """Handle the signup request."""
        serializer = serializers.UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user)
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.set_cookie('isLoggedIn', 'yes', max_age=settings.SESSION_COOKIE_AGE, samesite='Lax')
        return response


class LogoutView(views.APIView):
    """View to log the user out."""

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        """Handle the logout."""
        logout(request)
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('isLoggedIn')
        return response


class UserViewSet(viewsets.ViewSet):
    """ViewSet to create the action of getting the current (authenticate) user's stats and status."""

    permission_classes = (permissions.IsAuthenticated,)

    @action(methods=("GET",), detail=False, url_path="me")
    def get_current_user_data(self, request):
        """Method to get the current user's stats and status. (?)."""
        data = {
            "user": serializers.UserSerializer(request.user, context=dict(request=request)).data,
        }
        return Response(data)
