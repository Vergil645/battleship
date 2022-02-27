from typing import Set, Tuple, List
import random

from field import Field


class Ship(object):
    """
    Describes ship
    """
    hp: int  # count of not destroyed 'ship pipes'
    size: int
    x: int  # x-coordinate of starting point
    y: int  # y-coordinate of starting point
    rotation: int  # ship rotation

    def __init__(self, size: int, x: int, y: int, rotation: int):
        self.hp = size
        self.size = size
        self.x = x
        self.y = y
        self.rotation = rotation

    @property
    def occupied_cells(self) -> Set[Tuple[int, int]]:
        """
        :return: list of points occupied by ship
        """
        if self.rotation == 0:
            # East
            return set((self.x + dx, self.y) for dx in range(self.size))
        if self.rotation == 1:
            # South
            return set((self.x, self.y + dy) for dy in range(self.size))
        if self.rotation == 2:
            # West
            return set((self.x - dx, self.y) for dx in range(self.size))
        if self.rotation == 3:
            # North
            return set((self.x, self.y - dy) for dy in range(self.size))
        assert False, f'Invalid rotation: {self.rotation}'

    @property
    def occupied_and_nearby_cells(self) -> Set[Tuple[int, int]]:
        """
        :return: list of points occupied by the ship and all adjacent to them
        """
        return set((x + dx, y + dy)
                   for (x, y) in self.occupied_cells
                   for dx in range(-1, 2)
                   for dy in range(-1, 2))

    def receive_shot(self):
        assert self.hp > 0, 'Ship is already destroyed'
        self.hp -= 1

    def is_destroyed(self) -> bool:
        return self.hp == 0

    def fits(self, field: Field, existed_ships) -> bool:
        """
        :param field: field where ships will be placed
        :param existed_ships: ships that are already placed on field
        :return: True if we can place this ship on given field with others or False otherwise
        """
        for x, y in self.occupied_cells:
            # Check that ship is on field
            if not field.on_field(x, y):
                return False
        # Checks that ships are not touching
        return not any(not ship.occupied_and_nearby_cells.isdisjoint(self.occupied_cells)
                       for ship in existed_ships)

    @staticmethod
    def get_sizes(field: Field) -> List[int]:
        """
        :param field: field where ships will be placed
        :return: list of ships sizes for this field
        """
        m = 3 + 2 * (min(field.length, field.width) // 10)
        return [k for k in range(1, m) for _ in range(m - k)]

    @staticmethod
    def generate_ships(field: Field):
        """
        Generate random correct ships for given field
        :param field: field where ships will be placed
        :return: list of ships
        """
        # Ship sizes
        sizes = Ship.get_sizes(field)
        positions = Ship.generate_positions(field)
        # Already created ships
        ships = []
        # Index of current random position
        i = 0
        for size in reversed(sizes):
            created = False
            while i < len(positions):
                x, y, rotation = positions[i]
                i += 1
                new_ship = Ship(size, x, y, rotation)
                if new_ship.fits(field, ships):
                    ships.append(new_ship)
                    created = True
                    break
            if not created:
                assert False, f'Cannot generate ships with sizes {sizes} on the field {field.length}x{field.width}'
        return ships

    @staticmethod
    def generate_positions(field: Field) -> List[Tuple[int, int, int]]:
        """
        Generate all positions and rotations of ships in random order
        :param field: field where ships will be placed
        :return: list of positions and rotations
        """
        positions = [(x, y, rotation)
                     for x in range(field.length)
                     for y in range(field.width)
                     for rotation in range(4)]
        random.shuffle(positions)
        return positions
