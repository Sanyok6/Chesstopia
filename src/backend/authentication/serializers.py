from chess.models import ChessMatch
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers

from . import models

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for the creation of a User. Uses the User model that is active in the project."""

    class Meta:
        """Meta class for the :class:`UserCreateSerializer`.

        From :class:`authentication.models.CustomUser`(?), uses:
        :param username: 50 characters or fewer. Letters, digits and /@, /., /+, /-, or /_
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
    """Serializer for the stats and status of a user. Uses the User model that is active in the project."""

    password = None
    stats = serializers.SerializerMethodField()

    class Meta:
        """Meta class for the :class:`UserSerializer`.

        From :class:`authentication.models.CustomUser`(?), uses-
        :param id: /# TODO
        :type id: IntegerField
        :param username: 50 characters or fewer. Letters, digits and /@, /., /+, /-, or /_ only.
        :type username: CharField
        :param is_staff: Designates whether the user can log into this admin site.
        :type is_staff: BooleanField, optional
        :param is_playing: /# TODO
        :type is_playing: BooleanField, optional, default=False
        :param stats: /# TODO
        :type stats: SerializerMethodField
        """

        model = User
        fields = ('id', 'username', 'is_staff', 'is_playing', 'stats')

    def get_stats(self, user):
        """Return a dictionary of the user's Wins, Losses and Draws for Confusion Chess and Magic Chess."""
        queryset = ChessMatch.objects.filter(Q(white=user) | Q(black=user))
        confusion_chs_qs = queryset.filter(type="confusion_chess")
        magic_chs_qs = queryset.filter(type="magic_chess")

        return {
            "confusion_chess": {
                "wins": (
                    confusion_chs_qs.filter(white=user, result=1).count()
                    + confusion_chs_qs.filter(black=user, result=-1).count()
                ),
                "losses": (
                    confusion_chs_qs.filter(white=user, result=-1).count()
                    + confusion_chs_qs.filter(black=user, result=1).count()
                ),
                "draws": confusion_chs_qs.filter(result=0).count(),
            },
            "magic_chess": {
                "wins": (
                    magic_chs_qs.filter(white=user, result=1).count()
                    + magic_chs_qs.filter(black=user, result=-1).count()
                ),
                "losses": (
                    magic_chs_qs.filter(white=user, result=-1).count()
                    + magic_chs_qs.filter(black=user, result=1).count()
                ),
                "draws": magic_chs_qs.filter(result=0).count(),
            }
        }


class LoginSerializer(serializers.Serializer):
    """Serializer for login."""

    username = serializers.CharField()
    password = serializers.CharField()
