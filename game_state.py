from board import Board
from game_modes import GameModes

CHARACTERISTIC_BOARD = 650


class GameState:
    def __init__(self) -> None:
        self.__game_mode: GameModes = GameModes.hotseat
        self.__cell_board = 60
        self.__line_width = 2
        self.__move_first_player = True
        self.__board = Board(0)
        self.__figure_size = 0

    @property
    def board(self) -> Board:
        """Возвращает класс Board"""
        return self.__board

    @board.setter
    def board(self, board: Board) -> None:
        """Изменяет класс Board"""
        self.__board = board

    @property
    def game_mode(self) -> GameModes:
        """Возвращаем режим игры"""
        return self.__game_mode

    @game_mode.setter
    def game_mode(self, game_mode: GameModes) -> None:
        """Изменяет режим игры"""
        self.__game_mode = game_mode

    @property
    def move_first_player(self) -> bool:
        """Возвращает порядок хода"""
        return self.__move_first_player

    @move_first_player.setter
    def move_first_player(self, move_first_player: bool) -> None:
        """Изменяет порядок хода"""
        self.__move_first_player = move_first_player

    @property
    def cell_board(self) -> int:
        """Возвращает размер ячеек"""
        return self.__cell_board

    @property
    def line_width(self) -> int:
        """Возвращает ширину линии"""
        return self.__line_width

    @property
    def figure_size(self) -> int:
        """Возвращает размер фигур"""
        return self.__figure_size

    def characteristics_field(self, size: int) -> None:
        """Установка характеристик поля"""

        self.__cell_board = CHARACTERISTIC_BOARD // (size - 1)
        self.__figure_size = int(self.__cell_board * 0.9)
