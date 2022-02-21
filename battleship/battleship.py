from typing import Optional

from player import Player
from field import Field


class Battleship(object):
    turn: int
    players: [Player]

    def __init__(self, field_height: int, field_width: int, name: str):
        self.turn = 0
        self.players = [Player(name, Field(field_height, field_width)),
                        Player("AI", Field(field_height, field_width))]

    @property
    def winner(self) -> Optional[Player]:
        if self.players[0].ships_count == 0:
            return self.players[1]
        elif self.players[1].ships_count == 0:
            return self.players[0]
        else:
            return None

    @property
    def current_player(self):
        return self.players[self.turn]

    @property
    def next_player(self):
        return self.players[1 - self.turn]

    def make_shot(self, x: int, y: int):
        result = self.current_player.note_shot(x, y, *self.next_player.receive_shot(x, y))
        if result == "missing":
            self.turn = 1 - self.turn
