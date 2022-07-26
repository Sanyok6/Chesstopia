from rest_framework import serializers
from rest_framework.serializers import ValidationError

from authentication.serializers import UserSerializer
from . import models


class ChessMatchCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChessMatch
        fields = ('white', 'black', 'type')

    def validate(self, data):
        if not (data['white'] or data['black']):
            raise ValidationError('At least the white player or the black player needs to be specified')

        return data


class ChessMatchSerializer(ChessMatchCreateSerializer):
    white = UserSerializer()
    black = UserSerializer()

    class Meta(ChessMatchCreateSerializer.Meta):
        fields = '__all__'


class ChessMatchResultSerializer(serializers.ModelSerializer):
    result = serializers.IntegerField(allow_null=False, required=True)

    def validate_result(self, result):
        if result < -1 or result > 1:
            raise ValidationError('Result must be between -1 and 1 (inclusive)')

        return result

    class Meta:
        model = models.ChessMatch
        fields = ('result',)


class WebSocketActionSerializer(serializers.Serializer):
    action = serializers.CharField(required=True, allow_null=False)
    data = serializers.JSONField(required=True, allow_null=False)
