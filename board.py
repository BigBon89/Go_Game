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
    def game_field(self) -> list:
        return self.__game_field

    def check_rules(self) -> None:
        pass

    def get_group(self, rock_coordinate: tuple[int, int]) -> list[tuple[int, int]]:
        """
        Возвращает список координат клеток одной группы
        """
        result = []
        visited = set()
        player_id = self.__game_field[rock_coordinate[0]][rock_coordinate[1]]
        if player_id == 0:
            return result
        q = Queue()
        q.put(rock_coordinate)
        while not q.empty():
            pos = q.get()
            if pos in visited:
                continue
            visited.add(pos)
            result.append(pos)
            if self.__game_field[pos[0] + 1][pos[1]] == player_id:
                q.put((pos[0] + 1, pos[1]))
            if self.__game_field[pos[0] - 1][pos[1]] == player_id:
                q.put((pos[0] - 1, pos[1]))
            if self.__game_field[pos[0]][pos[1] + 1] == player_id:
                q.put((pos[0], pos[1] + 1))
            if self.__game_field[pos[0]][pos[1] - 1] == player_id:
                q.put((pos[0], pos[1] - 1))
        return result


    def __getitem__(self, index: int) -> list:
        return self.__game_field[index]

    def check_rock(self, x: int, y: int) -> bool:
        return self.__game_field[x][y] != 0

    def add_rock(self, x: int, y: int, move: int) -> None:
        self.__game_field[x][y] = move

    # def counting_nei