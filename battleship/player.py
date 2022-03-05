from typing import Optional, Tuple, List
from enum import Enum

from ship import Ship
from field import LEGEND_WIDTH, LEGEND_HEIGHT, Field

MENU_WIDTH = 14
MENU_HEIGHT = 5

LEGEND_MENU_HEIGHT = max(LEGEND_HEIGHT, MENU_HEIGHT)
LEGEND_MENU_WIDTH = LEGEND_WIDTH + 6 + MENU_WIDTH


class ShotResult(Enum):
    water = 0
    hit = 1
    killing = 2


class Player(object):
    """
    Describes battleship player
    """
    field: Field  # field with map and radar
    ships_count: int  # count of alive ships
    ship_matrix: List[List[Optional[Ship]]]  # ship layout matrix
    shots: int  # count of made shots
    hits: int  # count of hits

    def __init__(self, field: Field, ships: List[Ship]):
        self.field = field
        self.ships_count = len(ships)
        # Initialize ships_matrix
        self.ships_matrix = [[None] * field.width for _ in range(field.length)]
        for ship in ships:
            for x, y in ship.occupied_cells:
                # Cell (x, y) contains a ship
                self.ships_matrix[x][y] = ship
                self.field.map.set_ship(x, y)
        self.shots = 0
        self.hits = 0

    def check_point(self, x: int, y: int) -> bool:
        """
        Check that point is on field and is not already discovered
        """
        return self.field.on_field(x, y) and self.field.radar.is_empty(x, y)

    def mark_shot(self, x: int, y: int, result: ShotResult, target_ship: Optional[Ship]) -> ShotResult:
        """
        Process a shot, which was made by this player
        Pre: no more than 1 shot can be made into the same point
        :param x: x-coordinate of target point on enemy field
        :param y: y-coordinate of target point on enemy field
        :param result: result of the shot
        :param target_ship: killed enemy ship or None if no ship was destroyed
        :return: result of the shot
        """
        assert self.check_point(x, y), "Incorrect coordinates"
        self.shots += 1
        if result == ShotResult.water:
            # Mark a miss shot on radar
            self.field.radar.set_water(x, y)
        else:
            # Mark a hit on radar
            self.field.radar.set_hit(x, y)
            self.hits += 1
            if result == ShotResult.killing:
                assert target_ship is not None
                for x, y in target_ship.occupied_and_nearby_cells:
                    # Mark cells around destroyed ships on radar
                    if self.check_point(x, y):
                        self.field.radar.set_water(x, y)
        return result

    def receive_shot(self, x: int, y: int) -> Tuple[ShotResult, Optional[Ship]]:
        """
        Process a shot, which was made by enemy player
        Pre: no more than 1 shot can be made into the same point
        :param x: x-coordinate of target point on self field
        :param y: y-coordinate of target point on self field
        :return: result of the shot and killed ship or None if no ship was destroyed
        """
        ship = self.ships_matrix[x][y]
        if ship is None:
            # Mark a miss on map
            self.field.map.set_water(x, y)
            return ShotResult.water, None
        # Mark a hit on map
        self.field.map.set_hit(x, y)
        self.ships_matrix[x][y] = None
        ship.receive_shot()
        if ship.is_destroyed():
            # Ship is destroyed
            self.ships_count -= 1
            return ShotResult.killing, ship
        # Ship is not destroyed
        return ShotResult.hit, None

    @property
    def menu(self) -> List[str]:
        """
        :return: representation of menu with counts of shots, hits and misses
        """
        return [f'+------------+',
                f'| shots: {str(self.shots).rjust(3)} |',
                f'|  hits: {str(self.hits).rjust(3)} |',
                f'| water: {str(self.shots - self.hits).rjust(3)} |',
                f'+------------+']

    def display_legend_menu(self, screen_width: int) -> str:
        """
        :param screen_width: width of screen where legend and menu will be displayed
        :return: representation of the legend and the player menu
        """
        rows = list(map(lambda r1, r2: r1 + ' ' * 6 + r2, Field.legend(), self.menu))
        padding = ' ' * max(0, (screen_width - LEGEND_WIDTH - MENU_WIDTH - 6) // 2)
        return padding + ('\n' + padding).join(rows)
