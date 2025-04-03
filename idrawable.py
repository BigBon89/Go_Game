from abc import abstractmethod, ABC

from pygame import Surface


class IDrawable(ABC):
    """Интерфейс для объектов которые будут отрисовываться"""

    @abstractmethod
    def draw(self, surface: "Surface") -> None:
        pass
