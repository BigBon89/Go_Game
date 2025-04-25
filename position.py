from typing import NamedTuple, Self


class Position(NamedTuple):
    x: int
    y: int

    def inverted(self) -> Self:
        """Инвертирует x и y"""

        return Position(self.y, self.x)  # type: ignore[return-value]
