import pytest

from board import Board, Position


@pytest.fixture()
def data() -> "Board":
    board = Board(5)
    return board


def test_board_check_rock(data: Board) -> None:
    assert not data.check_rock(Position(0, 0))
    data.add_rock(Position(0, 0), 1)
    assert data.check_rock(Position(0, 0))


def test_board_add_rock(data: Board) -> None:
    data.add_rock(Position(2, 2), 1)
    assert data.game_field[2][2] == 1


def test_get_group_one_stone(data: Board) -> None:
    pos = Position(1, 1)
    data.add_rock(pos, 1)
    group = data.get_group(pos)
    assert group == [pos]


def test_get_group_a_few_stone(data: Board) -> None:
    stones = [Position(1, 1), Position(1, 2), Position(2, 1)]
    for pos in stones:
        data.add_rock(pos, 1)

    group = data.get_group(Position(1, 1))
    assert group is not None and set(group) == set(stones)


def test_has_void_true(data: Board) -> None:
    pos = Position(1, 1)
    data.add_rock(pos, 1)
    assert data.has_void([pos])


def test_has_void_false(data: Board) -> None:
    data.add_rock(Position(1, 1), 1)
    data.add_rock(Position(0, 1), 2)
    data.add_rock(Position(2, 1), 2)
    data.add_rock(Position(1, 0), 2)
    data.add_rock(Position(1, 2), 2)

    assert not data.has_void([Position(1, 1)])


def test_has_void_true_if_free_space(data: Board) -> None:
    data.add_rock(Position(0, 0), 1)
    assert data.has_void([Position(0, 0)])


def test_has_void_false_because_die(data: Board) -> None:
    data.add_rock(Position(2, 2), 1)
    for x, y in [(1, 2), (3, 2), (2, 1), (2, 3)]:
        data.add_rock(Position(x, y), 2)

    data.check_rules()
    assert not data.check_rock(Position(2, 2))


def test_get_count_score(data: Board) -> None:
    data.add_rock(Position(1, 1), 1)
    data.add_rock(Position(0, 1), 2)
    data.add_rock(Position(2, 1), 2)
    data.add_rock(Position(1, 0), 2)
    data.add_rock(Position(1, 2), 2)

    data.check_rules()
    assert data.get_count_score() == (1, 5)
