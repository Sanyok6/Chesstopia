import random

from django.conf import settings
from django.db import models
from django.utils.crypto import get_random_string


def generate_id():
    """Return a securely generated random string of 20 character from :meth:`django.utils.get_random_string`"""
    return get_random_string(20)


def generate_fen():
    """Generate the FEN for the board.

    Uses the Forsyth-Edwards Notation with seven pieces randomised from the list of Rook, Knight, Bishop and Queen.
    The seven pieces are the same for both players, but are shuffled after randomly generated. Active player, Castling
    Rights, en Passant Targets are reset to "w KQkq -", while halfmoves and fullmove are reset to 0 and 1 respectively.

    :return: Position of pieces in FEN (notation).
    :rtype: str
    """
    pieces = ["r", "n", "b", "q"]
    layout = ["k"]
    for p in range(7):
        layout.append(pieces[random.randint(0, len(pieces) - 1)])

    def get_random_layout():
        """Shuffle the non-pawn rank and format to FEN."""
        random.shuffle(layout)
        return str(layout).strip('[]').replace('\'', '').replace(', ', '')

    fen = get_random_layout()+"/pppppppp/8/8/8/8/PPPPPPPP/"+get_random_layout().upper()+" w KQkq - 0 1"
    return fen


class ChessMatch(models.Model):
    """Class for a chess match. Subclass of :class:`django.db.models.base.Model`."""

    CHESS_MATCH_TYPES = [
        ("confusion_chess", "Confusion chess"),
        ("magic_chess", "Magic chess")
    ]
    id = models.SlugField(allow_unicode=True, primary_key=True, default=generate_id)
    white = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
                              related_name="chess_match_white")
    black = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
                              related_name="chess_match_black")
    type = models.CharField(max_length=50, choices=CHESS_MATCH_TYPES)
    starting_pos = models.TextField(default=generate_fen)
    created_at = models.DateTimeField(auto_now_add=True)
    result = models.IntegerField(choices=((0, "Draw"), (1, "White wins"), (-1, "Black wins")), null=True, blank=True)
