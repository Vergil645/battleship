from enum import Enum
from string import ascii_uppercase

MIN_LENGTH = 5
MAX_LENGTH = 26

MIN_WIDTH = 5
MAX_WIDTH = 26

LEGEND_WIDTH = 14


class Cell(Enum):
    """
    Symbols on field
    """
    empty = '~'
    water = 'O'
    hit = 'X'
    ship = 'S'


class Table(object):
    """
    Describes a table of map or radar
    """
    length: int
    width: int
    content: [[Cell]]

    def __init__(self, length: int, width: int):
        self.length = length
        self.width = width
        self.content = [[Cell.empty for _ in range(width)] for _ in range(length)]

    def is_empty(self, x: int, y: int) -> bool:
        return self.content[x][y] == Cell.empty

    def set_water(self, x: int, y: int):
        self.content[x][y] = Cell.water

    def set_hit(self, x: int, y: int):
        self.content[x][y] = Cell.hit

    def set_ship(self, x: int, y: int):
        self.content[x][y] = Cell.ship

    @property
    def rows(self) -> [str]:
        """
        :return: representation of this table with coordinates by sides
        """
        padding = "  " if self.width < 10 else "   "
        num_len = 1 if self.width < 10 else 2
        result = [padding + " ".join(ascii_uppercase[:self.length])]
        for i in range(0, self.width):
            result.append(str(i + 1).rjust(num_len) + " " + " ".join(col[i].value for col in self.content))
        return result


class Field(object):
    """
    Describes player field: map and radar
    """
    length: int
    width: int
    map: Table
    radar: Table

    def __init__(self, length: int, width: int):
        self.length = length
        self.width = width
        self.map = Table(length, width)
        self.radar = Table(length, width)

    def on_field(self, x: int, y: int) -> bool:
        """
        :return: True if point (x, y) is on field and False otherwise
        """
        return 0 <= x < self.length and 0 <= y < self.width

    def display(self, screen_width) -> str:
        """
        :param screen_width: width of screen where field will be displayed
        :return: representation of the host player field
        """
        rows = list(map(lambda r1, r2: r1 + ' ' * 6 + r2, self.map.rows, self.radar.rows))
        padding = ' ' * max(0, (screen_width - len(rows[0])) // 2)
        return padding + ('\n' + padding).join(rows)

    @staticmethod
    def legend() -> [str]:
        return [f"+------------+",
                f"|   ship: {str(Cell.ship.value)}  |",
                f"|    hit: {str(Cell.hit.value)}  |",
                f"|  water: {str(Cell.water.value)}  |",
                f"+------------+"]
