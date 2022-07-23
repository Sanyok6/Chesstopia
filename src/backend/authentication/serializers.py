from django.contrib.auth import get_user_model, login
from rest_framework import serializers


User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, user_data):
        return User.objects.create_user(user_data['username'], user_data['email'], user_data['password'])


class UserSerializer(serializers.ModelSerializer):
    password = None
    email = None
    # profile_picture = serializers.ImageField(use_url=True)

    class Meta:
        model = User
        fields = ('username', 'is_staff')


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
