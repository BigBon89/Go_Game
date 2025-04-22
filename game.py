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
from widgets.button import Button, Color, Size


class Game:
    """Главный класс, отвечающий за игру"""

    def __init__(self) -> None:

        pygame.init()
        self._logger = Logger()
        self._logger.info("Create Game")
        self._initialization_step = 0

        self._surface = pygame.display.set_mode((1000, 800))
        self._clock = pygame.time.Clock()

        self._score = Score(self._logger)
        self.__state = GameState()
        self._rules = GameRules(state=self.__state,
                                logger=self._logger)
        self._graphic = GameGraphic(state=self.__state,
                                    score=self._score,
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

        self.__state.board = Board(size)
        self.__state.characteristics_field(size)
        self._initialization_step = 1
        self._logger.info(f"Field size set to {size}x{size}")

    def _select_gamemode(self, gamemode: GameModes) -> None:
        """Выбор игрового режима"""

        self.__state.game_mode = gamemode
        self._initialization_step = 2
        self._logger.info(f"Game mode select to {gamemode}")

    def refresh(self) -> None:
        """Обнуляет игровое поле"""

        for x in range(self.__state.board.size):
            for y in range(self.__state.board.size):
                self.__state.board.add_rock(Position(x, y), 0)
        self._logger.info("Board refreshed")

    def finish_game(self) -> None:
        """Выход главное"""

        self._save_scores()
        self._initialization_step = 0
        self.refresh()

    def _save_scores(self) -> None:
        """Сохранение текущих очков"""

        score_removed = self.__state.board.get_count_score()
        score_first_player = score_removed[0]
        score_second_player = score_removed[1]
        self._score.add_score(score_first_player)
        self._score.add_score(score_second_player)
        self._score.save_scores()
        self.__state.board.reset_removed_stones()

    def exit(self) -> None:
        """Выход из приложения"""

        self.finish_game()
        pygame.quit()
        self._logger.info("Close Game")
        exit()

    def run(self) -> None:
        """Запуск игры"""

        fields_buttons = [
            Button(position=Position(y, 100),
                   size=Size((200, 70)),
                   text=f"Размер поля {size}x{size}",
                   active_color=Color((160, 10, 50)),
                   inactive_color=Color((230, 230, 230)),
                   function=lambda s=size: self._select_field(s))
            for y, size in zip([150, 360, 570], [9, 13, 19])
        ]

        modes_buttons = [
            Button(position=Position(y, 100),
                   size=Size((260, 70)),
                   text=f"Режим игры {mode.name}",
                   active_color=Color((160, 10, 50)),
                   inactive_color=Color((230, 230, 230)),
                   function=lambda m=mode: self._select_gamemode(m))
            for y, mode in zip([90, 370, 650], GameModes)
        ]

        exit_button = Button(
            position=Position(775, 0),
            size=Size((70, 70)),
            text="Выйти",
            active_color=Color((160, 10, 50)),
            inactive_color=Color((230, 230, 230)),
            function=self.finish_game)

        while True:
            self._surface.fill((255, 255, 255))
            self._poll_events()

            if self._initialization_step == 0:
                for e in fields_buttons:
                    e.draw(self._surface)
            elif self._initialization_step == 1:
                for e in modes_buttons:
                    e.draw(self._surface)
            elif self._initialization_step == 2:
                self._rules.check_click()
                if self.__state.game_mode == GameModes.computer_random:
                    self._rules.random_computer_move()
                elif self.__state.game_mode == GameModes.computer_smart:
                    self._rules.smart_computer_move()

                self._graphic.draw(self._surface)
                exit_button.draw(self._surface)
                self.__state.board.check_rules()

            pygame.display.update()
            self._clock.tick(60)
