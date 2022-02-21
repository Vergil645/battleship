class Ship(object):
    hp: int
    size: int
    row: int
    col: int
    rotation: int

    def __init__(self, size: int, row: int, col: int, rotation: int):
        self.hp = size
        self.size = size
        self.row = row
        self.col = col
        self.rotation = rotation

    @property
    def occupied_cells(self) -> [(int, int)]:
        if self.rotation == 0:
            return [(self.row, self.col + y) for y in range(self.size)]
        elif self.rotation == 1:
            return [(self.row + x, self.col) for x in range(self.size)]
        elif self.rotation == 2:
            return [(self.row, self.col - y) for y in range(self.size)]
        else:
            return [(self.row - x, self.col) for x in range(self.size)]

    def handle_hit(self):
        self.hp -= 1
        if self.hp < 0:
            raise RuntimeError("Ship is already destroyed")

    def is_destroyed(self) -> bool:
        return self.hp == 0
