from enum import Enum


class GameModes(Enum):
    """Режимы игры"""

    hotseat = 0
    computer_random = 1
    computer_smart = 2