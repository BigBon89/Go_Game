import random

import pygame

from board import Board
from position import Position
from game_modes import GameModes
from game_state import GameState
from logger import Logger


class GameRules:
    def __init__(self, state: GameState, logger: Logger):
        self.new_board: Board = Board(0)
        self.all_board: dict[int, Board] = {9: Board(9),
                                            13: Board(13),
                                            19: Board(19)}
        self.__state = state
        self.__logger = logger
        self.last_step = [-1, -1]

    def check_click(self) -> None:
        """Ставит камень при клике на сетку"""

        if not pygame.mouse.get_pressed()[0] or (not self.__state.move_first_player and self.__state.game_mode != 0):
            return

        mouse_pos = Position(*pygame.mouse.get_pos())
        current_pos = Position(
            round((mouse_pos.x - self.__state.cell_board) / self.__state.cell_board),
            round((mouse_pos.y - self.__state.cell_board) / self.__state.cell_board)
        )

        if 0 <= current_pos.x < self.__state.board.size and 0 <= current_pos.y < self.__state.board.size:
            self.make_move(current_pos)

    def random_computer_move(self) -> None:
        """Делает случайный ход за компьютер"""

        if self.__state.move_first_player or self.__state.game_mode == GameModes.hotseat:
            return
        count = 0
        while True:
            position = Position(
                random.randint(0, self.__state.board.size - 1),
                random.randint(0, self.__state.board.size - 1),
            )
            if self.make_move(position):
                break
            count += 1

    def make_move(self, pos: Position) -> bool:
        """Делает ход за текущего игрока"""

        if self.__state.board.check_rock(
                pos.inverted()
        ):
            return False
        player_id = int(self.__state.move_first_player) + 1
        self.__state.board.add_rock(pos, player_id)
        self.__state.board.check_rules()
        self.__logger.info(
            f"The player {int(self.__state.move_first_player) + 1} made a move on the position "
            f"({pos.x}, {pos.y})"
        )
        self.__state.move_first_player = not self.__state.move_first_player

        return True

    def smart_computer_move(self) -> None:
        """Компьютер делает более умные ходы"""

        if self.__state.move_first_player or self.__state.game_mode != GameModes.computer_smart:
            return

        good_move = [-1, -1]
        for x in range(self.__state.board.size):
            for y in range(self.__state.board.size):
                pos = Position(x, y)
                if self.__state.board.check_rock(Position(x, y)):
                    continue

                if self._simulate_move(pos=pos, move=2) > 0:
                    good_move[0] = pos.x
                    good_move[1] = pos.y

        for x in range(self.__state.board.size):
            for y in range(self.__state.board.size):
                pos = Position(x, y)
                if self.__state.board.check_rock(Position(x, y)):
                    continue

                if self._simulate_move(pos=pos, move=1) > 0:
                    good_move[0] = pos.x
                    good_move[1] = pos.y

        if good_move[0] != -1:
            self.make_move(Position(good_move[0], good_move[1]))
            if good_move[0] == self.last_step[0] and good_move[1] == self.last_step[1]:
                self.random_computer_move()
            self.last_step[0] = good_move[0]
            self.last_step[1] = good_move[1]
            return
        self.random_computer_move()
        return

    def _simulate_move(self, pos: Position, move: int) -> int:
        """Симулирует ход"""
        if self.__state.board.check_rock(pos):
            return 0
        self.clone_field()
        self.new_board.add_rock(pos, move)

        before = self.new_board.get_tuple_removed_stones()[move % 2]
        self.new_board.check_rules()
        after = self.new_board.get_tuple_removed_stones()[move % 2]

        return after - before

    def clone_field(self) -> None:
        size = self.__state.board.size
        self.new_board = self.all_board[size]
        self.new_board.reset()
        for x in range(size):
            for y in range(size):
                value = self.__state.board.game_field[y][x]
                if value:
                    self.new_board.add_rock(Position(x, y), value)
