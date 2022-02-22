from typing import Set, Tuple
import random


class Ship(object):
    hp: int
    size: int
    x: int
    y: int
    rotation: int

    def __init__(self, size: int, x: int, y: int, rotation: int):
        self.hp = size
        self.size = size
        self.x = x
        self.y = y
        self.rotation = rotation

    @property
    def occupied_cells(self) -> Set[Tuple[int, int]]:
        if self.rotation == 0:
            return set((self.x + dx, self.y) for dx in range(self.size))
        elif self.rotation == 1:
            return set((self.x, self.y + dy) for dy in range(self.size))
        elif self.rotation == 2:
            return set((self.x - dx, self.y) for dx in range(self.size))
        elif self.rotation == 3:
            return set((self.x, self.y - dy) for dy in range(self.size))
        else:
            raise ValueError(f"Invalid rotation: {self.rotation}")

    @property
    def occupied_and_nearby_cells(self) -> Set[Tuple[int, int]]:
        return set((x + dx, y + dy)
                   for (x, y) in self.occupied_cells
                   for dx in range(-1, 2)
                   for dy in range(-1, 2))

    def receive_shot(self):
        if self.hp <= 0:
            raise RuntimeError("Ship is already destroyed")
        self.hp -= 1

    def is_destroyed(self) -> bool:
        return self.hp == 0

    def fits(self, field_length: int, field_width: int, existed_ships) -> bool:
        for x, y in self.occupied_cells:
            if not (0 <= x < field_length and 0 <= y < field_width):
                return False
        return not any(not ship.occupied_and_nearby_cells.isdisjoint(self.occupied_cells)
                       for ship in existed_ships)

    @staticmethod
    def get_sizes(field_length: int, field_width: int) -> [int]:
        m = 3 + 2 * (min(field_length, field_width) // 10)
        return [k for k in range(1, m) for _ in range(m - k)]

    @staticmethod
    def generate_ships(field_length: int, field_width: int):
        sizes = Ship.get_sizes(field_length, field_width)
        positions = Ship.generate_positions(field_length, field_width)
        ships = []
        i = 0
        for size in reversed(sizes):
            created = False
            while i < len(positions):
                x, y, rotation = positions[i]
                i += 1
                new_ship = Ship(size, x, y, rotation)
                if new_ship.fits(field_length, field_width, ships):
                    ships.append(new_ship)
                    created = True
                    break
            if not created:
                print(ships)
                raise RuntimeError(f"Cannot generate ships with sizes {sizes} "
                                   f"on the field {field_length}x{field_width}")
        return ships

    @staticmethod
    def generate_positions(field_length: int, field_width: int) -> [(int, int, int)]:
        positions = [(x, y, rotation)
                     for x in range(field_length)
                     for y in range(field_width)
                     for rotation in range(4)]
        random.shuffle(positions)
        return positions
