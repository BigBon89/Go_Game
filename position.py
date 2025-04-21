from typing import NamedTuple


class Position(NamedTuple):
    x: int
    y: int

    def inverted(self) -> 'Position':
        """Инвертирует x и y"""

        return Position(self.y, self.x)
