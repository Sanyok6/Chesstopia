import json
from asgiref.sync import async_to_sync
from django.core.exceptions import ObjectDoesNotExist
from channels.generic.websocket import WebsocketConsumer

from chess.models import ChessMatch


chess_matches = {}
"""
{
    game_id: {
            "white: user,
            "black": user,
        }
}
"""


class ChessMatchConsumer(WebsocketConsumer):
    def connect(self):
        user = self.scope['user']
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.game_group_name = 'chess_match_%s' % self.game_id

        if user.is_authenticated:
            try:
                self.chess_match = ChessMatch.obects.get(id=self.game_id)
                async_to_sync(self.channel_layer.group_add)(
                    self.game_group_name,
                    self.channel_name
                )
                self.accept()
            except ObjectDoesNotExist:
                return self.close(404)  # Not found

        else:
            self.close(401)  # Unauthorized

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.game_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
