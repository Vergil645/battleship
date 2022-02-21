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

    def add_ship(self, ship: Ship):
        self.ship = ship

    @staticmethod
    def empty_cell():  # -> ???
        return Cell(None)


class Field(object):
    height: int
    width: int
    cells: [[Cell]]
    radar: [[int]]

    def __init__(self, height: int, width: int):
        if height < MIN_HEIGHT or height > MAX_HEIGHT:
            raise ValueError(f"Field height must be in range [{MIN_HEIGHT}; {MAX_HEIGHT}]")
        if width < MIN_WIDTH or width > MAX_WIDTH:
            raise ValueError(f"Field width must be in range [{MIN_WIDTH}; {MAX_HEIGHT}]")
        self.height = height
        self.width = width
        self.cells = [[Cell.empty_cell() for _ in range(width)] for _ in range(height)]
        self.radar = [[0 for _ in range(width)] for _ in range(height)]

    def check_ship_fits(self, ship: Ship) -> bool:
        for (x, y) in ship.occupied_cells:
            if x < 0 or x >= self.height or y < 0 or y >= self.width:
                return False
            if not self.cells[x][y].is_empty():
                return False
        return True

    def add_ship(self, ship: Ship):
        if not self.check_ship_fits(ship):
            raise ValueError("Ship cannot pe placed on the field")
        for (x, y) in ship.occupied_cells:
            self.cells[x][y].add_ship(ship)

    def draw(self):
        pass
