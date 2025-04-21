from typing import NamedTuple


class Position(NamedTuple):
    x: int
    y: int

    def inverted(self):
        return Position(self.y, self.x)
