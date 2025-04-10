from queue import Queue
from typing import Optional, NamedTuple


class Position(NamedTuple):
    x: int
    y: int


class Board:
    """Класс отвечающий за доску"""

    def __init__(self, size: int) -> None:
        self._size = size
        self.__game_field = [[0] * self._size for _ in range(self._size)]

    @property
    def size(self) -> int:
        return self._size

    @property
    def game_field(self) -> list[list[int]]:
        return self.__game_field

    def check_rules(self) -> None:
        """
        Проверяет правила игры
        """

        for x in range(self._size - 1):
            for y in range(self._size - 1):
                group = self.get_group(Position(x, y))
                if group is None:
                    continue
                if self.has_void(group):
                    continue
                for cell in group:
                    self.__game_field[cell[0]][cell[1]] = 0

    def has_void(self, group: list[Position]) -> bool:
        """
        Проверяет есть ли пустые соседние клетки у группы камней
        """
        for pos in group:
            poses = [
                Position(pos.x + 1, pos.y),
                Position(pos.x - 1, pos.y),
                Position(pos.x, pos.y + 1),
                Position(pos.x, pos.y - 1),
            ]
            for new_pos in poses:
                if (
                        new_pos.x < 0
                        or new_pos.x >= self._size
                        or new_pos.y < 0
                        or new_pos.y >= self._size
                ):
                    continue
                if self.__game_field[new_pos.x][new_pos.y] == 0:
                    return True
        return False

    def get_group(
            self, rock_coordinate: Position
    ) -> Optional[list[Position]]:
        """
        Возвращает список координат клеток одной группы
        """

        result = []
        visited = set()
        player_id = self.__game_field[rock_coordinate[0]][rock_coordinate[1]]
        if player_id == 0:
            return None
        q: Queue[Position] = Queue()
        q.put(rock_coordinate)

        while not q.empty():
            pos = q.get()
            if pos in visited:
                continue
            visited.add(pos)
            result.append(pos)
            poses = [
                Position(pos.x + 1, pos.y),
                Position(pos.x - 1, pos.y),
                Position(pos.x, pos.y + 1),
                Position(pos.x, pos.y - 1)
            ]
            for new_pos in poses:
                if (
                        new_pos.x < 0
                        or new_pos.x >= self._size
                        or new_pos.y < 0
                        or new_pos.y >= self._size

                ):
                    continue
                if self.__game_field[new_pos.x][new_pos.y] == player_id:
                    q.put(new_pos)
        return result

    def __getitem__(self, index: int) -> list[int]:
        return self.__game_field[index]

    def check_rock(self, x: int, y: int) -> bool:
        """Проверяет есть ли камень на переданных координатах"""

        return self.__game_field[x][y] != 0

    def add_rock(self, position: Position, move: int) -> None:
        """Добавляет камень конкретного игрока на заданные координаты"""

        self.__game_field[position.y][position.x] = move
