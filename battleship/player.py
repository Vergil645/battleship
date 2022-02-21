from typing import Optional

from ship import Ship
from field import Field


class Player(object):
    name: str
    ships_count: int
    field: Field

    def __init__(self, name: str, field: Field):
        self.name = name
        self.ships_count = 0
        self.field = field

    def note_shot(self, x: int, y: int, hit: bool, target_ship: Optional[Ship]) -> str:
        if not hit:
            self.field.radar[x][y] = 1
            return "miss"
        else:
            self.field.radar[x][y] = 2
            if target_ship is None:
                return "hit"
            else:
                for (x, y) in target_ship.occupied_and_nearby_cells:
                    if self.field.point_on_field(x, y) and self.field.radar[x][y] == 0:
                        self.field.radar[x][y] = 1
                return "killed"

    def receive_shot(self, x: int, y: int) -> (bool, Optional[Ship]):
        cell = self.field.map[x][y]
        if cell.is_empty():
            return False, None
        else:
            target_ship = cell.ship
            cell.ship = None
            target_ship.receive_shot()
            if target_ship.is_destroyed():
                self.ships_count -= 1
            return True, target_ship if target_ship.is_destroyed() else None
