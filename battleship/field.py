from typing import Optional
from ship import Ship

MIN_HEIGHT = 5
MAX_HEIGHT = 26

MIN_WIDTH = 5
MAX_WIDTH = 26


class Cell(object):
    ship: Optional[Ship]

    def __init__(self, ship: Optional[Ship]):
        self.ship = ship

    def is_empty(self) -> bool:
        return self.ship is None

    @staticmethod
    def empty_cell():  # -> ???
        return Cell(None)


class Field(object):
    height: int
    width: int
    map: [[Cell]]
    radar: [[int]]

    def __init__(self, height: int, width: int):
        assert MIN_HEIGHT <= height <= MAX_HEIGHT, \
            f"Field height must be in range [{MIN_HEIGHT}; {MAX_HEIGHT}], actually: {height}"
        assert MIN_WIDTH <= width <= MAX_WIDTH, \
            f"Field width must be in range [{MIN_WIDTH}; {MAX_HEIGHT}], actually: {width}"
        self.height = height
        self.width = width
        self.map = [[Cell.empty_cell() for _ in range(width)] for _ in range(height)]
        self.radar = [[0 for _ in range(width)] for _ in range(height)]

    def point_on_field(self, x: int, y: int):
        return 0 <= x < self.height and 0 <= y < self.width

    def ship_fits(self, ship: Ship) -> bool:
        for (x, y) in ship.occupied_cells:
            if not self.point_on_field(x, y):
                return False
        for (x, y) in ship.occupied_and_nearby_cells:
            if self.point_on_field(x, y) and not self.map[x][y].is_empty():
                return False
        return True

    def add_ship(self, ship: Ship):
        assert self.ship_fits(ship), "Ship cannot pe placed on the field"
        for (x, y) in ship.occupied_cells:
            self.map[x][y].ship = ship

    def draw(self) -> str:  # TODO
        pass

    def generate_ships(self, rule):  # TODO
        pass
