from rest_framework import serializers
from rest_framework.serializers import ValidationError

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
    class Meta(ChessMatchCreateSerializer.Meta):
        fields = '__all__'


class ChessMatchResultSerializer(serializers.ModelSerializer):
    result = serializers.IntegerField(allow_null=False, required=True)

    def validate_result(self, result):
        if result < -1 or result > 1:
            raise ValidationError('Result must be between -1 and 1 (inclusive)')

        return result

    def update(self, chess_match, data):
        if self.context['request'].user not in (chess_match.white, chess_match.black):
            raise ValidationError("You did not play this game")

        if not chess_match.white or not chess_match.black:
            raise ValidationError("This match hasn't been played yet")

        chess_match.result = data['result']

        return super().update(chess_match, data)

    class Meta:
        model = models.ChessMatch
        fields = ('result',)


class WebSocketActionSerializer(serializers.Serializer):
    action = serializers.CharField(required=True, allow_null=False)
    data = serializers.JSONField(required=True, allow_null=False)
