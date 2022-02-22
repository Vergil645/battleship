from typing import Optional

from player import Player
from ship import Ship


class Battleship(object):
    turn: int
    players: [Player]

    def __init__(self, field_length: int, field_width: int):
        self.turn = 0
        self.players = [Player(field_length, field_width, Ship.generate_ships(field_length, field_width)),
                        Player(field_length, field_width, Ship.generate_ships(field_length, field_width))]

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
        result = self.current_player.mark_shot(x, y, *self.next_player.receive_shot(x, y))
        if result == "miss":
            self.turn = 1 - self.turn
