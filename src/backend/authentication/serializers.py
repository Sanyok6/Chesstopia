from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers

from chess.models import ChessMatch
from . import models


User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for the creation of a User. Uses the User model that is active in the
    project.
    """
    class Meta:
        """Meta class for the :class:`UserCreateSerializer`.

        From CustomUser, uses:
        :param username: 50 characters or fewer. Letters, digits and @, ., +, -, or _
        only.
        :type username: CharField
        :param password: 128 characters or fewer.
        :type password: CharField
        """
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, user_data):
        """From the `user_data`, create the user and hash the password."""
        return User.objects.create_user(user_data['username'], password=user_data['password'])


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the stats of a user. Uses the User model that is active in the
    project.
    """
    password = None
    stats = serializers.SerializerMethodField()

    class Meta:
        """Meta class for the :class:`UserSerializer`.

        From CustomUser, uses:
        :param id:
        :type id: IntegerField
        :param username: 50 characters or fewer. Letters, digits and @, ., +, -, or _
        only.
        :type username: CharField
        :param is_staff: Designates whether the user can log into this admin site.
        :type is_staff: BooleanField, optional
        :param is_playing:
        :type is_playing: BooleanField, optional
        :param stats:
        :type stats: SerializerMethodField
        """
        model = User
        fields = ('id', 'username', 'is_staff', 'is_playing', 'stats')

    def get_stats(self, user):
        """Return a dictionary of the user's Wins, Losses and Draws for Confusion Chess
        and Magic Chess.
        """
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


class LoginSerializer(serializers.Serializer):
    """Serializer for login."""
    username = serializers.CharField()
    password = serializers.CharField()
