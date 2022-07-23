from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from rest_framework import permissions, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from . import serializers


class LoginView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
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
        response.set_cookie('isLoggedIn', 'yes', expires=settings.SESSION_COOKIE_AGE)

        return response


class SignupView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = serializers.UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user)
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.set_cookie('isLoggedIn', 'yes', expires=settings.SESSION_COOKIE_AGE)
        return response


class LogoutView(views.APIView):
    def post(self, request):
        logout(request)
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('isLoggedIn')
        return response


class UserViewSet(viewsets.ViewSet):

    @action(methods=("GET",), detail=False, url_path="me")
    def get_current_user_data(self, request):
        data = {
            "user": serializers.UserSerializer(request.user, context=dict(request=request)).data,
        }
        return Response(data)
