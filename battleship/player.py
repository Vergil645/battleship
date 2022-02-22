from typing import Optional

from ship import Ship
from table import Table


class Player(object):
    field_length: int
    field_width: int

    map: Table
    radar: Table

    ships_count: int
    ship_matrix: [[Optional[Ship]]]

    shots: int
    hits: int

    def __init__(self, field_length: int, field_width: int, ships: [Ship]):
        self.field_length = field_length
        self.field_width = field_width

        self.map = Table(field_length, field_width)
        self.radar = Table(field_length, field_width)

        self.ships_count = len(ships)
        self.ships_matrix = [[None for _ in range(field_width)] for _ in range(field_length)]
        for ship in ships:
            for x, y in ship.occupied_cells:
                self.ships_matrix[x][y] = ship
                self.map.set(x, y, '□')

        self.shots = 0
        self.hits = 0

    def mark_shot(self, x: int, y: int, hit: bool, target_ship: Optional[Ship]) -> str:
        self.shots += 1
        if not hit:
            if self.radar.is_empty(x, y):
                self.radar.set(x, y, 'O')
            return "miss"
        else:
            self.radar.set(x, y, 'X')
            self.hits += 1
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

    def display_field(self, screen_width) -> str:
        rows = list(map(lambda r1, r2: r1 + ' ' * 4 + r2, self.map.draw_rows(), self.radar.draw_rows()))
        padding = ' ' * max(0, (screen_width - len(rows[0])) // 2)
        return padding + ('\n' + padding).join(rows)

    @property
    def menu(self) -> [str]:
        return [f"+------------+",
                f"| shots: {str(self.shots).rjust(3)} |",
                f"|  hits: {str(self.hits).rjust(3)} |",
                f"| water: {str(self.shots - self.hits).rjust(3)} |",
                f"+------------+"]
