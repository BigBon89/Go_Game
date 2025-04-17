import pygame
import pygame.freetype

from board import Board, Position
from game_graphic import GameGraphic
from game_modes import GameModes
from game_rules import GameRules
from game_state import GameState
from widgets.button import Button
from logger import Logger
from score import Score


class Game:
    """Главный класс, отвечающий за игру"""

    def __init__(self) -> None:
        pygame.init()
        self.logger = Logger()
        self.logger.info("Create Game")
        self.initialization_step = 0

        self.surface = pygame.display.set_mode((1000, 800))
        self.clock = pygame.time.Clock()

        self.score = Score()
        self.state = GameState()
        self.rules = GameRules(self.state, self.logger)
        self.graphic = GameGraphic(self.state, self.score)


    def _poll_events(self) -> None:
        """Обработка событий окна"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()

    def _select_field(self, size: int) -> None:
        """Выбор параметров для поля"""

        self.state.board = Board(size)
        self.state.characteristics_field(size)
        self.initialization_step = 1
        self.logger.info(f"Field size set to {size}x{size}")

    def _select_gamemode(self, gamemode: int) -> None:
        """Выбор игрового режима"""

        self.state.game_mode = gamemode
        self.initialization_step = 2
        self.logger.info(f"Game mode select to {gamemode}")

    def refresh(self) -> None:
        """Обнуляет игровое поле"""

        for x in range(self.state.board.size):
            for y in range(self.state.board.size):
                self.state.board.add_rock(Position(x, y), 0)
        self.logger.info("Board refreshed")

    def finish_game(self) -> None:
        """Выход главное"""

        self.score.save_scores()
        self.initialization_step = 0
        self.refresh()

    def exit(self) -> None:
        """Выход из приложения"""

        self.finish_game()
        pygame.quit()
        self.logger.info("Close Game")
        exit()

    def run(self) -> None:
        """Запуск игры"""


        pos_y = [155, 230, 310]
        buttons = {
            "exit": Button(position=Position(775, 0),
                           size=(70, 70),
                           text="Выйти",
                           active_color=(160, 10, 50),
                           inactive_color=(230, 230, 230),
                           function=self.finish_game),
            "fields": [
                Button(position=Position(765, y),
                       size=(230, 70),
                       text=f"Размер поля {size}x{size}",
                       active_color=(160, 10, 50),
                       inactive_color=(230, 230, 230),
                       function=lambda s=size: self._select_field(s)
                       )
                for y, size in zip(pos_y, [9, 13, 19])
            ],
            "modes": [
                Button(position=Position(765, y),
                       size=(230, 70),
                       text=f"Режим игры {mode.name}",
                       active_color=(160, 10, 50),
                       inactive_color=(230, 230, 230),
                       function=lambda m=mode.value: self._select_gamemode(m)
                       )
                for y, mode in zip(pos_y, GameModes)
            ]
        }

        while True:
            self.surface.fill((255, 255, 255))
            self._poll_events()

            if self.initialization_step == 0:
                for e in buttons["fields"]:
                    e.draw(self.surface)
            elif self.initialization_step == 1:
                for e in buttons["modes"]:
                    e.draw(self.surface)
            elif self.initialization_step == 2:
                self.rules.check_click()
                self.rules.computer_move()
                self.graphic.draw(self.surface)
                buttons["exit"].draw(self.surface)
                self.state.board.check_rules()

            pygame.display.update()
            self.clock.tick(60)
