from mypy.types import NewType

from fundamental.logger import Logger
from game.game_state import GameState
from position import Position

Step = NewType("Step", list[tuple[int, Position]])


class Save:
    def __init__(self,
                 state: GameState,
                 logger: Logger) -> None:
        self._state = state
        self._logger = logger
        self._history: Step = Step([])
        self._number_move: int = 0

    def add_step_player(self, position: Position, move: int) -> None:
        """Добавляет ход первого игрока"""
        if self._number_move >= len(self._history):
            self._history.append((move, position.inverted()))
        else:
            self._history[self._number_move] = (move, position.inverted())
        self._number_move += 1

    def step_back(self, count: int = 0) -> None:
        """Возвращает предыдущий ход"""
        count = count
        if self._number_move == 0:
            return
        self._state.board.reset()
        game_field = self._state.board.game_field
        for num_step in range(self._number_move - 1):
            move, step_first = self._history[num_step]
            game_field[step_first.x][step_first.y] = move
            self._state.board.check_rules()
        self._number_move -= 1
        self._state.move_first_player = True if not self._state.move_first_player else False
        if self._state.game_mode.value != 0 and count == 0:
            count += 1
            self.step_back(count)
        self._logger.info("Step back")

    def step_next(self) -> None:
        """Возвращает ход вперед"""
        if self._number_move < len(self._history):
            move, step = self._history[self._number_move]
            self._state.board[step.x][step.y] = move
            self._state.board.check_rules()
            self._number_move += 1
            self._logger.info("Step next")
