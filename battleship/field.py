from enum import Enum
from string import ascii_uppercase
from typing import List

MIN_LENGTH = 5
MAX_LENGTH = 26

MIN_WIDTH = 5
MAX_WIDTH = 26

LEGEND_WIDTH = 14
LEGEND_HEIGHT = 5


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
    content: List[List[Cell]]

    def __init__(self, length: int, width: int):
        self.length = length
        self.width = width
        self.content = [[Cell.empty] * width for _ in range(length)]

    def is_empty(self, x: int, y: int) -> bool:
        return self.content[x][y] == Cell.empty

    def set_water(self, x: int, y: int):
        self.content[x][y] = Cell.water

    def set_hit(self, x: int, y: int):
        self.content[x][y] = Cell.hit

    def set_ship(self, x: int, y: int):
        self.content[x][y] = Cell.ship

    @property
    def height_on_screen(self) -> int:
        return 1 + self.width

    @property
    def width_on_screen(self) -> int:
        num_len = 1 if self.width < 10 else 2
        return num_len + 2 * self.length

    @property
    def rows(self) -> List[str]:
        """
        :return: representation of this table with coordinates by sides
        """
        padding = '  ' if self.width < 10 else '   '
        num_len = 1 if self.width < 10 else 2
        result = [padding + ' '.join(ascii_uppercase[:self.length])]
        for i in range(self.width):
            result.append(str(i + 1).rjust(num_len) + ' ' + ' '.join(col[i].value for col in self.content))
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

    @property
    def height_on_screen(self) -> int:
        return max(self.map.height_on_screen, self.radar.height_on_screen)

    @property
    def width_on_screen(self) -> int:
        return self.map.width_on_screen + 6 + self.radar.width_on_screen

    def display(self, screen_width) -> str:
        """
        :param screen_width: width of screen where field will be displayed
        :return: representation of the host player field
        """
        rows = list(map(lambda r1, r2: r1 + ' ' * 6 + r2, self.map.rows, self.radar.rows))
        padding = ' ' * max(0, (screen_width - len(rows[0])) // 2)
        return padding + ('\n' + padding).join(rows)

    @staticmethod
    def legend() -> List[str]:
        return [f'+------------+',
                f'|   ship: {str(Cell.ship.value)}  |',
                f'|    hit: {str(Cell.hit.value)}  |',
                f'|  water: {str(Cell.water.value)}  |',
                f'+------------+']
