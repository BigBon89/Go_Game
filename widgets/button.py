import time

import pygame
import pygame.freetype
from pygame import Surface
from typing import Callable, Any, Optional

from board import Position
from idrawable import IDrawable
from widgets.text import Text


class Button(IDrawable):
    def __init__(
            self,
            position: Position,
            size: tuple[int, int],
            text: str,
            active_color: tuple[int, int, int],
            inactive_color: tuple[int, int, int],
            function: Optional[Callable[..., Any]] = None,
    ) -> None:
        self._position = position
        self._size = size
        self._width = size[0]
        self._height = size[1]
        self.active_color = active_color
        self.inactive_color = inactive_color
        self._text_object = Text(
            (position[0] + 5, position[1] + 5), (0, 0, 0), text, 16
        )
        self.function = function

    @property
    def position(self) -> Position:
        return self._position

    @position.setter
    def position(self, position: Position) -> None:
        if position.x < 0 or position.y < 0:
            raise ValueError("Координаты x и y не могут быть отрицательными")
        self._position = position

    @property
    def size(self) -> tuple[int, int]:
        return self._size

    @size.setter
    def size(self, size: tuple[int, int]) -> None:
        if size[0] < 0 or size[1] < 0:
            raise ValueError("Размеры x и y не могут быть отрицательными")
        self._size = size

    def hover(self) -> bool:
        mouse = pygame.mouse.get_pos()
        x = self._position.x
        y = self._position.y
        return x < mouse[0] < x + self._width and y < mouse[1] < y + self._height

    def draw(self, surface: "Surface") -> None:
        x = self._position.x
        y = self._position.y
        if self.hover():
            pygame.draw.rect(
                surface, self.active_color, (x, y, self._width, self._height)
            )
        else:
            pygame.draw.rect(
                surface, self.inactive_color, (x, y, self._width, self._height)
            )
        self._text_object.draw(surface)
        if self.pressed() and self.function is not None:
            self.function()

    def pressed(self) -> bool:
        mouse_click = pygame.mouse.get_pressed()
        if not mouse_click[0]:
            return False
        mouse_pos = Position(*pygame.mouse.get_pos())
        if (
            self._position.x < mouse_pos.x < self._position.x + self._size[0] and
            self._position.y < mouse_pos.y < self._position.y + self._size[1]
        ):
            time.sleep(0.2)
            return True
        return False

    def __bool__(self) -> bool:
        return self.pressed()
