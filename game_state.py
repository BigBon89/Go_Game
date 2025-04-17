from board import Board
from game_modes import GameModes
from score import Score


class GameState:
    def __init__(self) -> None:
        self.game_mode: int = GameModes.hotseat.value
        self.cell_board = 60
        self.line_width = 2
        self.init_step = 0
        self.move_first_player = True
        self.board = Board(0)
        self.scoreboard = Score()
        self.figure_size = None

    def characteristics_field(self, size: int) -> None:
        """Установка характеристик поля"""

        self.cell_board = 650 // (size - 1)
        self.figure_size = int(self.cell_board * 0.9)
