from queue import Queue


class Board:
    """Класс отвечающий за доску"""

    def __init__(self, size: int) -> None:
        self._size = size  # Размер игрового поля
        self.__game_field = [[0] * self._size for _ in range(self._size)]  # Игровое поле

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

        for i in range(self._size):
            for j in range(self._size):
                group = self.get_group((i, j))
                if group is None:
                    continue
                if self.has_void(group):
                    continue
                for cell in group:
                    self.__game_field[cell[0]][cell[1]] = 0

    def has_void(self, group: list[tuple[int, int]]) -> bool:
        """
        Проверяет есть ли пустые соседние клетки у группы камней
        """

        for pos in group:
            poses = [(pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]), (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)]
            for new_pos in poses:
                if new_pos[0] < 0 or new_pos[0] >= self._size or new_pos[1] < 0 or new_pos[1] >= self._size:
                    continue
                if self.__game_field[new_pos[0]][new_pos[1]] == 0:
                    return True
        return False

    def get_group(self, rock_coordinate: tuple[int, int]) -> list[tuple[int, int]] | None:
        """
        Возвращает список координат клеток одной группы
        """

        result = []
        visited = set()
        player_id = self.__game_field[rock_coordinate[0]][rock_coordinate[1]]
        if player_id == 0:
            return None
        q: "Queue[tuple[int, int]]" = Queue()
        q.put(rock_coordinate)
        while not q.empty():
            pos = q.get()
            if pos in visited:
                continue
            visited.add(pos)
            result.append(pos)
            poses = [(pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]), (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)]
            for new_pos in poses:
                if new_pos[0] < 0 or new_pos[0] >= self._size or new_pos[1] < 0 or new_pos[1] >= self._size:
                    continue
                if self.__game_field[new_pos[0]][new_pos[1]] == player_id:
                    q.put((new_pos[0], new_pos[1]))
        return result

    def __getitem__(self, index: int) -> list[int]:
        return self.__game_field[index]

    def check_rock(self, x: int, y: int) -> bool:
        """Проверяет есть ли камень на переданных координатах"""

        return self.__game_field[x][y] != 0

    def add_rock(self, x: int, y: int, move: int) -> None:
        """Добавляет камень конкретного игрока на заданные координаты"""

        self.__game_field[x][y] = move

    # def counting_nei
