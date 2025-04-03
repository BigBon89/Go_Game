import pytest

from board import Board

@pytest.fixture()
def data() -> "Board":
    board = Board(5)
    return board

def test_board_check_rock(data) -> None:
    assert data.check_rock(0, 0) == False
