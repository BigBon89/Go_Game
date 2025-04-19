import pygame
import pygame.freetype

from board import Board
from logger import Logger
from position import Position
from game_graphic import GameGraphic
from game_modes import GameModes
from game_rules import GameRules
from game_state import GameState
from score import Score
from widgets.button import Button


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
        self.rules = GameRules(state=self.state,
                               logger=self.logger)
        self.graphic = GameGraphic(state=self.state,
                                   score=self.score,
                                   filename1="image/rock.png",
                                   filename2="image/monster.png"
                                   )

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

        self._save_scores()
        self.initialization_step = 0
        self.refresh()

    def _save_scores(self) -> None:
        """Сохранение текущих очков"""

        score_removed = self.state.board.get_count_score()
        score_first_player = score_removed[0]
        score_second_player = score_removed[1]
        self.score.add_score(score_first_player)
        self.score.add_score(score_second_player)
        self.score.save_scores()
        self.state.board.reset_removed_stones()

    def exit(self) -> None:
        """Выход из приложения"""

        self.finish_game()
        pygame.quit()
        self.logger.info("Close Game")
        exit()

    def run(self) -> None:
        """Запуск игры"""

        pos_y = [155, 230, 310]
        fields_buttons = [
            Button(position=Position(765, y),
                   size=(230, 70),
                   text=f"Размер поля {size}x{size}",
                   active_color=(160, 10, 50),
                   inactive_color=(230, 230, 230),
                   function=lambda s=size: self._select_field(s))
            for y, size in zip(pos_y, [9, 13, 19])
        ]

        modes_buttons = [
            Button(position=Position(765, y),
                   size=(230, 70),
                   text=f"Режим игры {mode.name}",
                   active_color=(160, 10, 50),
                   inactive_color=(230, 230, 230),
                   function=lambda m=mode.value: self._select_gamemode(m))
            for y, mode in zip(pos_y, GameModes)
        ]

        exit_button = Button(position=Position(775, 0),
                             size=(70, 70),
                             text="Выйти",
                             active_color=(160, 10, 50),
                             inactive_color=(230, 230, 230),
                             function=self.finish_game)

        while True:
            self.surface.fill((255, 255, 255))
            self._poll_events()

            if self.initialization_step == 0:
                for e in fields_buttons:
                    e.draw(self.surface)
            elif self.initialization_step == 1:
                for e in modes_buttons:
                    e.draw(self.surface)
            elif self.initialization_step == 2:
                self.rules.check_click()
                if self.state.game_mode == GameModes.computer_random.value:
                    self.rules.random_computer_move()
                elif self.state.game_mode == GameModes.computer_smart.value:
                    self.rules.smart_computer_move()

                self.graphic.draw(self.surface)
                exit_button.draw(self.surface)
                self.state.board.check_rules()

            pygame.display.update()
            self.clock.tick(60)
