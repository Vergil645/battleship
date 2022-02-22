from typing import Optional
import itertools

from ship import Ship
from table import Table


class Player(object):
    ships_count: int
    field_length: int
    field_width: int
    map: Table
    radar: Table
    ship_matrix: [[Optional[Ship]]]

    def __init__(self, field_length: int, field_width: int, ships: [Ship]):
        self.ships_count = len(ships)

        self.field_length = field_length
        self.field_width = field_width
        self.map = Table(field_length, field_width)
        self.radar = Table(field_length, field_width)

        self.ships_matrix = [[None for _ in range(field_width)] for _ in range(field_length)]
        for ship in ships:
            for x, y in ship.occupied_cells:
                self.ships_matrix[x][y] = ship
                self.map.set(x, y, '□')

    def mark_shot(self, x: int, y: int, hit: bool, target_ship: Optional[Ship]) -> str:
        if not hit:
            self.radar.set(x, y, 'O')
            return "miss"
        else:
            self.radar.set(x, y, 'X')
            if target_ship is None:
                return "hit"
            else:
                for x, y in target_ship.occupied_and_nearby_cells:
                    if 0 <= x < self.field_length and 0 <= y < self.field_width and self.radar.is_empty(x, y):
                        self.radar.set(x, y, 'O')
                return "killing"

    def receive_shot(self, x: int, y: int) -> (bool, Optional[Ship]):
        ship = self.ships_matrix[x][y]
        if ship is None:
            self.map.set(x, y, 'O')
            return False, None
        else:
            self.map.set(x, y, 'X')
            self.ships_matrix[x][y] = None
            ship.receive_shot()
            if ship.is_destroyed():
                self.ships_count -= 1
            return True, ship if ship.is_destroyed() else None

    def display_str(self, screen_width) -> str:  # TODO
        tmp1 = map(lambda r1, r2: r1 + "    " + r2, self.map.draw_rows(), self.radar.draw_rows())
        return "\n".join(tmp1)
