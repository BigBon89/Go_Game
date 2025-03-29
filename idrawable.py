from abc import abstractmethod, ABC

from pygame import Surface


class IDrawable(ABC):
    @abstractmethod
    def draw(self, surface: "Surface"):
        pass
