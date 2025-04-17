import pygame
import pygame.freetype
from pygame import Surface

from idrawable import IDrawable


class Text(IDrawable):
    def __init__(
        self,
        position: tuple[int, int],
        color: tuple[int, int, int],
        text: str,
        font_size: int,
    ) -> None:
        self._position = position
        self._color = color
        self._text = text
        self._font = pygame.freetype.Font("assets/Verdana.ttf", font_size)

    def draw(self, surface: "Surface") -> None:
        self._font.render_to(surface, self._position, self._text, self._color)

    @property
    def text(self) -> str:
        return self._text

    @property
    def position(self) -> tuple[int, int]:
        return self._position
