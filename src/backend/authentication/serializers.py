from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers

from chess.models import ChessMatch
from . import models


User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, user_data):
        return User.objects.create_user(user_data['username'], password=user_data['password'])


class UserSerializer(serializers.ModelSerializer):
    password = None
    stats = serializers.SerializerMethodField()

    def get_stats(self, user):
        queryset = ChessMatch.objects.filter(Q(white=user) | Q(black=user))
        return {
            "confusion_chess": {
                "wins": queryset.filter(type="confusion_chess", result=1).count(),
                "losses": queryset.filter(type="confusion_chess", result=-1).count(),
                "draws": queryset.filter(type="confusion_chess", result=0).count(),
            },
            "magic_chess": {
                "wins": queryset.filter(type="magic_chess", result=1).count(),
                "losses": queryset.filter(type="magic_chess", result=-1).count(),
                "draws": queryset.filter(type="magic_chess", result=0).count(),
            }
        }

    class Meta:
        model = User
        fields = ('id', 'username', 'is_staff', 'is_playing', 'stats')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
