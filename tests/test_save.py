from typing import Self

import pytest

from fundamental.board import Board
from game.game_state import GameState
from position import Position
from save import Save


@pytest.fixture()
def board() -> 'Board':
    board = Board(9)
    return board

@pytest.fixture()
def state() -> 'GameState':
    state = GameState()
    return state

@pytest.fixture()
def save(state: GameState) -> 'Save':
    save = Save(state)
    return save

def test_step_back(state: GameState, board: Board, save: Save):
    state.board = board
    state.board.add_rock(Position(1, 1), 1)
    save.add_step_player(Position(1, 1), 1)
    state.board.add_rock(Position(1, 2), 2)
    save.add_step_player(Position(1, 2), 2)
    state.board.add_rock(Position(1, 3), 1)
    save.add_step_player(Position(1, 3), 1)
    state.board.add_rock(Position(1, 4), 2)
    save.add_step_player(Position(1, 4), 2)
    save.step_back()

    assert state.board.game_field[4][1] == 0


def test_step_next(state: GameState, board: Board, save: Save):
    state.board = board
    state.board.add_rock(Position(1, 1), 1)
    save.add_step_player(Position(1, 1), 1)
    state.board.add_rock(Position(1, 2), 2)
    save.add_step_player(Position(1, 2), 2)
    state.board.add_rock(Position(1, 3), 1)
    save.add_step_player(Position(1, 3), 1)
    state.board.add_rock(Position(1, 4), 2)
    save.add_step_player(Position(1, 4), 2)
    save.step_back()
    save.step_back()
    save.step_next()
    save.step_next()

    assert state.board.game_field[4][1] == 2
    assert state.board.game_field[3][1] == 1