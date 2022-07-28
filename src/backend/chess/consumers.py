import json
from asgiref.sync import async_to_sync
from django.core.exceptions import ObjectDoesNotExist
from channels.generic.websocket import WebsocketConsumer

from chess.models import ChessMatch
from .serializers import WebSocketActionSerializer, ChessMatchSerializer, ChessMatchResultSerializer


class ChessMatchConsumer(WebsocketConsumer):
    def connect(self):
        user = self.scope['user']
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.game_group_name = 'match_%s' % self.game_id

        if user.is_authenticated:
            try:
                self.chess_match = ChessMatch.objects.get(id=self.game_id)
                async_to_sync(self.channel_layer.group_add)(
                    self.game_group_name,
                    self.channel_name
                )

                if self.chess_match.white and not self.chess_match.black and self.chess_match.white != user:
                    self.chess_match.black = user

                else:
                    self.chess_match.white = user

                self.chess_match.save()
                self.accept()

                if self.chess_match.white and self.chess_match.black:
                    async_to_sync(self.channel_layer.group_send)(
                        self.game_group_name,
                        {
                            'type': 'game_start',
                            'payload': ChessMatchSerializer(self.chess_match).data
                        }
                    )

            except ObjectDoesNotExist:
                return self.close(404)  # Not found

        else:
            self.close(401)  # Unauthorized

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.game_group_name,
            self.channel_name
        )

    def dispatch_named_event(self, event_name, payload, extra_params={}):
        """A helper function to dispatch an event with a name specified"""

        data = {
            'event': event_name.upper(),
            'payload': payload,
            **extra_params
        }
        self.send(text_data=json.dumps(data))

    def dispatch_error(self, payload, extra_params={}):
        self.dispatch_named_event('ERROR', payload, extra_params)

    def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.decoder.JSONDecodeError:
            return self.dispatch_named_event('ERROR', {'detail': 'Invalid JSON data'})
        serializer = WebSocketActionSerializer(data=data)

        chess_match = self.chess_match
        if serializer.is_valid():
            validated_data = serializer.data
            action = validated_data['action'].upper()

            if action == 'MAKE_MOVE':
                async_to_sync(self.channel_layer.group_send)(
                    self.game_group_name,
                    {
                        'type': 'make_move',
                        'payload': validated_data['data']
                    }
                )

            elif action == 'SET_RESULT':
                chess_match.refresh_from_db()

                if self.scope['user'] not in (chess_match.white, chess_match.black):
                    return self.dispatch_error({'detail': 'You did not play this game'})

                if not chess_match.white or not chess_match.black:
                    return self.dispatch_error({'detail': "This match hasn't been played yet"})

                if chess_match.result is not None:
                    return self.dispatch_error({'detail': 'The result of this match is already set'})

                match_result = ChessMatchResultSerializer(chess_match, data=validated_data['data'],
                                                          partial=True)
                if match_result.is_valid():
                    match_result.save()
                else:
                    self.dispatch_error(match_result.errors)
            else:
                self.dispatch_error({'detail': 'Invalid action'})

        else:
            self.dispatch_error(serializer.errors)

    def make_move(self, event):
        self.dispatch_named_event('CREATE_MOVE', event['payload'])

    def game_start(self, event):
        self.dispatch_named_event('GAME_START', event['payload'])
