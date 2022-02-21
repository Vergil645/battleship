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
    def occupied_cells(self) -> [(int, int)]:
        if self.rotation == 0:
            return [(self.x, self.y + dy) for dy in range(self.size)]
        elif self.rotation == 1:
            return [(self.x + dx, self.y) for dx in range(self.size)]
        elif self.rotation == 2:
            return [(self.x, self.y - dy) for dy in range(self.size)]
        else:
            return [(self.x - dx, self.y) for dx in range(self.size)]

    @property
    def occupied_and_nearby_cells(self) -> [(int, int)]:
        return [(x + dx, y + dy)
                for (x, y) in self.occupied_cells
                for dx in range(-1, 2)
                for dy in range(-1, 2)]

    def receive_shot(self):
        assert self.hp > 0, "Ship is already destroyed"
        self.hp -= 1

    def is_destroyed(self) -> bool:
        return self.hp == 0
