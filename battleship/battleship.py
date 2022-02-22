from typing import Optional

from player import Player
from ship import Ship


class Battleship(object):
    turn: int
    players: [Player]
    field_length: int
    field_width: int
    message: str

    def __init__(self, field_length: int, field_width: int):
        self.turn = 0
        self.players = [Player(field_length, field_width, Ship.generate_ships(field_length, field_width)),
                        Player(field_length, field_width, Ship.generate_ships(field_length, field_width))]
        self.field_length = field_length
        self.field_width = field_width
        self.message = ""

    @property
    def winner(self) -> Optional[int]:
        if self.players[0].ships_count == 0:
            return 1
        elif self.players[1].ships_count == 0:
            return 0
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
            self.message = "Miss!"
            self.turn = 1 - self.turn
        elif result == "hit":
            self.message = "Hit! Make additional turn!"
        else:
            self.message = "Killing! Make additional turn!"

    @property
    def field_height(self) -> int:
        return self.field_width + 1

    def display_player_field(self, screen_width: int) -> str:
        return self.players[0].display_field(screen_width)

    @property
    def message_height(self) -> int:
        return 1 if self.message else 0

    def display_message(self, screen_width: int) -> str:
        padding = ' ' * max(0, (screen_width - len(self.message)) // 2)
        result = padding + self.message + '\n' if self.message else ""
        self.message = ""
        return result

    @property
    def menu_height(self) -> int:
        return 5

    def display_menu(self, screen_width: int) -> str:
        padding = ' ' * max(0, (screen_width - 14) // 2)
        return padding + ('\n' + padding).join(self.players[0].menu)
