import random

import pygame

from position import Position
from game_modes import GameModes
from game_state import GameState
from logger import Logger

class GameRules:
    def __init__(self, state: GameState, logger: Logger):
        self.state = state
        self.logger = logger

    def check_click(self) -> None:
        """Ставит камень при клике на сетку"""

        if not pygame.mouse.get_pressed()[0] or (not self.state.move_first_player and self.state.game_mode != 0):
            return

        mouse_pos = Position(*pygame.mouse.get_pos())
        current_pos = Position(
            round((mouse_pos.x - self.state.cell_board) / self.state.cell_board),
            round((mouse_pos.y - self.state.cell_board) / self.state.cell_board)
        )

        if 0 <= current_pos.x < self.state.board.size and 0 <= current_pos.y < self.state.board.size:
            self.make_move(current_pos)

    def computer_move(self) -> None:
        """Делает ход за компьютер"""

        if self.state.move_first_player or self.state.game_mode == GameModes.hotseat.value:
            return

        while True:
            position = Position(
                random.randint(0, self.state.board.size - 1),
                random.randint(0, self.state.board.size - 1),
            )
            if self.make_move(position):
                break

    def make_move(self, pos: Position) -> bool:
        """Делает ход за текущего игрока"""

        if self.state.board.check_rock(
                Position(
                    pos.y,
                    pos.x
                )
        ):
            return False

        self.state.move_first_player = not self.state.move_first_player
        self.state.board.add_rock(pos, self.state.move_first_player + 1)
        self.logger.info(
            f"The player {int(self.state.move_first_player) + 1} made a move on the position "
            f"({pos.x}, {pos.y})"
        )
        return True

