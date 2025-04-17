import copy
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

    def random_computer_move(self) -> None:
        """Делает случайный ход за компьютер"""

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

    def smart_computer_move(self) -> None:
        """Компьютер делает более умные ходы"""

        if self.state.move_first_player or self.state.game_mode != GameModes.computer_smart.value:
            return

        for x in range(self.state.board.size):
            for y in range(self.state.board.size):
                pos = Position(x, y)
                if self.state.board.check_rock(Position(x, y)):
                    continue

                if self._simulate_move(pos) > 0:
                    self.make_move(pos)
                    return
        self.random_computer_move()

    def _simulate_move(self, pos: Position) -> int:
        """Симулирует ход компьютера"""

        copy_board = copy.deepcopy(self.state.board)
        current_removed = self.state.board.get_tuple_removed_stones()[0]

        copy_board.add_rock(pos, 2)
        copy_board.check_rules()
        new_removed = copy_board.get_tuple_removed_stones()[0]

        difference = new_removed - current_removed

        return difference