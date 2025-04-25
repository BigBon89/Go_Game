import time

import pygame
import pygame.freetype
from pygame import Surface
from typing import Callable, Any, Optional, NewType

from board import Position
from idrawable import IDrawable
from widgets.text import Text

Color = NewType('Color', tuple[int, int, int])
Size = NewType('Size', tuple[int, int])


class Button(IDrawable):
    def __init__(
            self,
            position: Position,
            size: Size,
            text: str,
            active_color: Color,
            inactive_color: Color,
            function: Optional[Callable[..., Any]] = None,
    ) -> None:
        self._position = position
        self._width = size[0]
        self._height = size[1]
        self._active_color = active_color
        self._inactive_color = inactive_color
        self.__text = text
        self._text_object: Text
        self._set_text_position()
        self.function = function

    @property
    def position(self) -> Position:
        return self._position

    @position.setter
    def position(self, position: Position) -> None:
        if position.x < 0 or position.y < 0:
            raise ValueError("Координаты x и y не могут быть отрицательными")
        self._position = position

    def get_size(self) -> tuple[int, int]:
        """Размер кнопки"""
        return self._width, self._height

    def set_width(self, size: int) -> None:
        """Задать ширину кнопки"""

        if size < 0:
            raise ValueError("Размеры x не может быть отрицательными")
        self._width = size

    def set_height(self, size: int) -> None:
        """Задать высоту кнопки"""

        if size < 0:
            raise ValueError("Размер y не может быть отрицательными")
        self._height = size

    def _set_text_position(self) -> None:
        """Обновить позицию текста для центрирования"""

        font_size = 16
        font = pygame.freetype.SysFont(None, font_size)
        text_rect = font.get_rect(self.__text)

        if self._width > 100:
            position = Position(
                self._position.x + (self._width - text_rect.width) // 2 - 5,
                self._position.y + (self._height - text_rect.height) // 2
            )
        else:
            position = Position(
                self._position.x + (self._width - text_rect.width) // 2,
                self._position.y + (self._height - text_rect.height) // 2
            )
        self._text_object = Text(position=position, color=(0, 0, 0), text=self.__text, font_size=font_size)

    def hover(self) -> bool:
        """Проверка, что курсор навели на кнопку"""

        mouse = pygame.mouse.get_pos()
        x = self._position.x
        y = self._position.y
        return x < mouse[0] < x + self._width and y < mouse[1] < y + self._height

    def draw(self, surface: Surface) -> None:
        """Отрисовка кнопки"""

        x = self._position.x
        y = self._position.y
        if self.hover():
            pygame.draw.rect(
                surface=surface, color=self._active_color, rect=(x, y, self._width, self._height)
            )
        else:
            pygame.draw.rect(
                surface=surface, color=self._inactive_color, rect=(x, y, self._width, self._height)
            )
        self._text_object.draw(surface)
        if self.pressed() and self.function is not None:
            self.function()

    def pressed(self) -> bool:
        """Проверка нажатия на кнопку"""
        mouse_click = pygame.mouse.get_pressed()
        if not mouse_click[0]:
            return False
        mouse_pos = Position(*pygame.mouse.get_pos())
        if (
                self._position.x < mouse_pos.x < self._position.x + self._width and
                self._position.y < mouse_pos.y < self._position.y + self._height
        ):
            time.sleep(0.2)
            return True
        return False

    def __bool__(self) -> bool:
        return self.pressed()
