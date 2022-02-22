from string import ascii_uppercase

MIN_LENGTH = 5
MAX_LENGTH = 26

MIN_WIDTH = 5
MAX_WIDTH = 26

EMPTY = '≋'


class Table(object):
    length: int
    width: int
    content: [[str]]

    def __init__(self, length: int, width: int):
        if not MIN_LENGTH <= length <= MAX_LENGTH:
            raise ValueError(f"Field height must be in range [{MIN_LENGTH}; {MAX_LENGTH}], "
                             f"actually: {length}")
        if not MIN_WIDTH <= width <= MAX_WIDTH:
            raise ValueError(f"Field width must be in range [{MIN_WIDTH}; {MAX_WIDTH}], "
                             f"actually: {width}")
        self.length = length
        self.width = width
        self.content = [[EMPTY for _ in range(width)] for _ in range(length)]

    def set(self, x: int, y: int, value: str):
        if len(value) != 1:
            raise ValueError("Length of content in table cell must be 1")
        self.content[x][y] = value

    def is_empty(self, x: int, y: int) -> bool:
        return self.content[x][y] == EMPTY

    def draw_rows(self) -> [str]:
        padding = "  " if self.width < 10 else "   "
        num_len = 1 if self.width < 10 else 2
        result = [padding + ascii_uppercase[:self.length]]
        for i in range(1, self.width + 1):
            result.append(str(i).rjust(num_len) + " " + "".join(col[i - 1] for col in self.content))
        return result

