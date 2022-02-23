from typing import Optional

from player import Player, ShotResult
from field import Field
from ship import Ship

MESSAGE_HEIGHT = 1
LEGEND_MENU_HEIGHT = 5


class Battleship(object):
    """
    Describes session of battleship game
    """
    turn: int  # number of current player
    host: int  # number of player how plays on this machine
    players: [Player]  # list of players
    messages: [str]  # list of messages for players
    field_length: int
    field_width: int

    def __init__(self, field_length: int, field_width: int, host: int = 0):
        self.turn = 0
        self.host = host
        player_field_0 = Field(field_length, field_width)
        player_field_1 = Field(field_length, field_width)
        # Create Player objects with empty fields and randomly generated ships
        self.players = [Player(player_field_0, Ship.generate_ships(player_field_0)),
                        Player(player_field_1, Ship.generate_ships(player_field_1))]
        self.messages = ["", ""]
        self.field_length = field_length
        self.field_width = field_width

    @property
    def winner(self) -> Optional[int]:
        """
        :return: number of winning player or None if game is not over yet
        """
        if self.players[0].ships_count == 0:
            # Player 1 wins
            return 1
        elif self.players[1].ships_count == 0:
            # Player 0 wins
            return 0
        else:
            return None

    @property
    def current_player(self) -> Player:
        """
        :return: current player object
        """
        return self.players[self.turn]

    @property
    def next_player(self) -> Player:
        """
        :return: next player object
        """
        return self.players[1 - self.turn]

    @property
    def host_player(self) -> Player:
        """
        :return: host player object
        """
        return self.players[self.host]

    def make_shot(self, x: int, y: int):
        """
        Make turn between players or doing anything if game is already over
        :param x: x-coordinate of target point on enemy field
        :param y: y-coordinate of target point on enemy field
        """
        # Check if game is over
        if self.winner is not None:
            # Do nothing
            return
        if not 0 <= x < self.field_length or not 0 <= y < self.field_width:
            # Said that coordinates is incorrect
            self.messages[self.turn] = "Point is not on field. Try again."
            return
        # Make shot
        result = self.current_player.mark_shot(x, y, *self.next_player.receive_shot(x, y))
        # Process result of shot and create appropriate messages
        if result == ShotResult.water:
            self.messages[self.turn] = "You missed."
            self.turn = 1 - self.turn
            return
        if result == ShotResult.hit:
            self.messages[self.turn] = "You hit. Shoot again!"
        elif result == ShotResult.killing:
            self.messages[self.turn] = "You destroyed enemy ship. Shoot again!"
        else:
            assert False, f"Unhandled ShotResult: {result}"
        if self.next_player.ships_count == 0:
            self.messages[self.turn] = "You win!"
            self.messages[1 - self.turn] = "You lose!"

    @property
    def field_height(self) -> int:
        """
        :return: height of field on screen
        """
        return self.field_width + 1

    def display_host_field(self, screen_width: int) -> str:
        """
        :param screen_width: width of screen where field will be displayed
        :return: representation of the host player field
        """
        return self.host_player.field.display(screen_width)

    def display_host_message(self, screen_width: int) -> str:
        """
        :param screen_width: width of screen where message will be displayed
        :return: representation of the host player message
        """
        message = self.messages[self.host]
        padding = ' ' * max(0, (screen_width - len(message)) // 2)
        result = padding + message + '\n' if message else ""
        return result

    def display_host_legend_menu(self, screen_width: int) -> str:
        """
        :param screen_width: width of screen where legend and menu will be displayed
        :return: representation of the legend and the host player menu
        """
        return self.host_player.display_legend_menu(screen_width)
