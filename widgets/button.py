import time

import pygame
import pygame.freetype
from pygame import Surface

from idrawable import IDrawable
from widgets.text import Text


class Button(IDrawable):
    def __init__(self, position: tuple,
                 size: tuple,
                 text: str,
                 active_color: tuple,
                 inactive_color: tuple,
                 function: callable = None) -> None:
        self._position = position
        self._size = size
        self._width = size[0]
        self._height = size[1]
        self.active_color = active_color
        self.inactive_color = inactive_color
        self._text_object = Text((position[0] + 5, position[1] + 5), (0, 0, 0), text, 16)
        self.function = function

    @property
    def position(self) -> tuple:
        return self._position

    @position.setter
    def position(self, position: tuple) -> None:
        if position[0] < 0 or position[1] < 0:
            raise ValueError("Координаты x и y не могут быть отрицательными")
        self._position = position

    @property
    def size(self) -> tuple:
        return self._size

    @size.setter
    def size(self, size: tuple) -> None:
        if size[0] < 0 or size[1] < 0:
            raise ValueError("Размеры x и y не могут быть отрицательными")
        self._size = size

    def hover(self) -> bool:
        mouse = pygame.mouse.get_pos()
        x = self._position[0]
        y = self._position[1]
        return x < mouse[0] < x + self._width and y < mouse[1] < y + self._height

    def draw(self, surface: 'Surface') -> None:
        x = self._position[0]
        y = self._position[1]
        if self.hover():
            pygame.draw.rect(surface, self.active_color, (x, y, self._width, self._height))
        else:
            pygame.draw.rect(surface, self.inactive_color, (x, y, self._width, self._height))
        self._text_object.draw(surface)
        if self.pressed() and self.function is not None:
            self.function()

    def pressed(self) -> bool:
        mouse_click = pygame.mouse.get_pressed()
        if not mouse_click[0]:
            return False
        mouse_pos = pygame.mouse.get_pos()
        if self._position[0] < mouse_pos[0] < self._position[0] + self._size[0] and \
                self._position[1] < mouse_pos[1] < self._position[1] + self._size[1]:
            time.sleep(0.2)
            return True
        return False

    def __bool__(self) -> bool:
        return self.pressed()
