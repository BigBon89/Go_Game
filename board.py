from queue import Queue
from typing import Optional

from position import Position


class Board:
    """Класс отвечающий за доску"""

    def __init__(self, size: int) -> None:
        self._size = size
        self.__game_field = [[0] * self._size for _ in range(self._size)]
        self._removed_stones_player = [0, 0]
        self._score_stone_player = [0, 0]

    @property
    def size(self) -> int:
        """Возвращает размер игрового поля"""

        return self._size

    @property
    def game_field(self) -> list[list[int]]:
        """Возвращает игровое поле"""

        return self.__game_field

    def check_rules(self) -> None:
        """
        Проверяет правила игры
        """

        for x in range(self._size):
            for y in range(self._size):
                group = self.get_group(Position(x, y))
                if group is None:
                    continue
                if self.has_void(group):
                    continue

                player = self.__game_field[group[0].x][group[0].y]
                for cell in group:
                    self.__game_field[cell[0]][cell[1]] = 0
                if player == 1:
                    self._removed_stones_player[0] += len(group)
                elif player == 2:
                    self._removed_stones_player[1] += len(group)

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

    def get_group(self, rock_coordinate: Position) -> Optional[list[Position]]:
        """
        Возвращает список координат клеток одной группы
        """

        result = []
        visited = set()
        player_id = self.__game_field[rock_coordinate.x][rock_coordinate.y]
        if player_id == 0:
            return None
        queue: Queue[Position] = Queue()
        queue.put(rock_coordinate)

        while not queue.empty():
            position = queue.get()
            if position in visited:
                continue
            visited.add(position)
            result.append(position)
            poses = [
                Position(position.x + 1, position.y),
                Position(position.x - 1, position.y),
                Position(position.x, position.y + 1),
                Position(position.x, position.y - 1)
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
                    queue.put(new_pos)
        return result

    def __getitem__(self, index: int) -> list[int]:
        return self.__game_field[index]

    def check_rock(self, position: Position) -> bool:
        """Проверяет есть ли камень на переданных координатах"""

        return self.__game_field[position.x][position.y] != 0

    def add_rock(self, position: Position, move: int) -> None:
        """Добавляет камень конкретного игрока на заданные координаты"""

        if move == 1:
            self._score_stone_player[0] += 1
        elif move == 2:
            self._score_stone_player[1] += 1
        self.__game_field[position.y][position.x] = move

    def get_tuple_removed_stones(self) -> tuple:
        """Возвращает счетчики удаленных камней"""

        return self._removed_stones_player[0], self._removed_stones_player[1]

    def reset_removed_stones(self) -> None:
        """Сбрасывает счетчик удаленных камней"""

        self._removed_stones_player[0] = 0
        self._removed_stones_player[1] = 0

    def get_count_score(self) -> tuple[int, int]:
        return (self._removed_stones_player[1] + self._score_stone_player[0],
                self._removed_stones_player[0] + self._score_stone_player[1])
