import random
from enum import Enum

import pygame
from pygame import Surface

from board import Board, Position
from widgets.button import Button
from logger import Logger


class GameModes(Enum):
    """Режимы игры"""

    hotseat = 0
    computer_random = 1
    computer_smart = 2


class Game:
    """Главный класс отвечающий за игру"""

    def __init__(self) -> None:
        self._game_mode: int = GameModes.hotseat.value
        self._cell_board = 60  # Размер доски
        self._line_width = 2  # Ширина линий поля
        self._initialization_step = 0
        self._move_first_player = True
        self._board = Board(0)

        self.rock = pygame.image.load("image/rock.png")
        self.monster = pygame.image.load("image/monster.png")
        self.logger = Logger()
        self.logger.info("Create Game")

    def draw(self, surface: Surface) -> None:
        """Отрисовка игрового поля, включая сетку и камни"""

        for x in range(self._board.size):
            pygame.draw.line(
                surface=surface,
                color=(0, 0, 0),
                start_pos=(self._cell_board, self._cell_board + x * self._cell_board),
                end_pos=(
                    self._cell_board + (self._board.size - 1) * self._cell_board,
                    self._cell_board + x * self._cell_board),
                width=self._line_width
            )

            pygame.draw.line(
                surface=surface,
                color=(0, 0, 0),
                start_pos=(self._cell_board + x * self._cell_board, self._cell_board),
                end_pos=(
                    self._cell_board + x * self._cell_board,
                    self._cell_board + (self._board.size - 1) * self._cell_board),
                width=self._line_width
            )

        for x in range(self._board.size):
            for y in range(self._board.size):
                if self._board[x][y] == 0:
                    continue

                index_x = self._cell_board + y * self._cell_board - self.FIGURE_SIZE // 2
                index_y = self._cell_board + x * self._cell_board - self.FIGURE_SIZE // 2

                if self._board[x][y] == 1:
                    surface.blit(self.stone_black, (index_x, index_y))
                else:
                    surface.blit(self.stone_white, (index_x, index_y))

    def _computer_move(self) -> None:
        """Делает ход за компьютер"""

        if self._move_first_player:
            return
        if self._game_mode == GameModes.hotseat.value:
            return

        while True:
            point = Position(
                random.randint(0, self._board.size - 1),
                random.randint(0, self._board.size - 1),
            )
            if self._board.check_rock(point):
                continue
            self._board.game_field[point.y][point.x] = 2
            self._move_first_player = not self._move_first_player
            break

    def check_click(self) -> None:
        """Ставит камень при клике на сетку"""

        if not pygame.mouse.get_pressed()[0]:
            return

        if not self._move_first_player and self._game_mode != 0:
            return
        mouse_pos = Position(*pygame.mouse.get_pos())
        position = self._cell_board - (self._cell_board - self._line_width) / 2

        if (
                min(mouse_pos.x, mouse_pos.y) < position
                or max(mouse_pos.x, mouse_pos.y) >= position * 2 * self._board.size
        ):
            return

        current_position = Position(
            round((mouse_pos.x - self._cell_board) / self._cell_board),
            round((mouse_pos.y - self._cell_board) / self._cell_board))

        if not (0 <= current_position.x < self._board.size and 0 <= current_position.y < self._board.size):
            return

        if self._board.check_rock(current_position):
            return

        self._move_first_player = not self._move_first_player
        self._board.add_rock(current_position, self._move_first_player + 1)
        self.logger.info(f"click on field, position {current_position.x}, {current_position.y}")

    def _poll_events(self) -> None:
        """Обработка событий окна"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass

    def __signal_button_select_field(self, size: int) -> None:
        """Событие при клике на кнопку"""

        self._board = Board(size)
        self.characteristics_field(size)
        self.logger.info("Changing the field size to 9x9")

    def characteristics_field(self, size: int) -> None:
        """Изменяет характеристики поля"""

        self._cell_board = 650 // (size - 1)
        self.FIGURE_SIZE = int(self._cell_board * 0.9)
        self.stone_black = pygame.transform.scale(
            self.rock, (self.FIGURE_SIZE, self.FIGURE_SIZE)
        )
        self.stone_white = pygame.transform.scale(
            self.monster, (self.FIGURE_SIZE, self.FIGURE_SIZE)
        )
        self._initialization_step = 2

    def refresh(self) -> None:
        for x in range(self._board.size):
            for y in range(self._board.size):
                self._board.add_rock(Position(x, y), 0)
        self.logger.info("Field Refresh")

    def exit(self) -> None:
        pygame.quit()
        self.logger.info("Close Game")
        exit(0)

    def run(self) -> None:
        """Запуск игры"""

        pygame.init()
        clock = pygame.time.Clock()
        window_size = (1000, 800)
        surface = pygame.display.set_mode(window_size)

        button_exit = Button(
            position=Position(775, 0),
            size=(70, 70),
            text="Выйти",
            active_color=(160, 10, 50),
            inactive_color=(230, 230, 230),
            function=self.exit
        )
        button_refresh = Button(
            position=Position(775, 75),
            size=(90, 70),
            text="Обновить",
            active_color=(160, 10, 50),
            inactive_color=(230, 230, 230),
            function=self.refresh,
        )
        button_change_field9 = Button(
            position=Position(765, 155),
            size=(230, 70),
            text="Изменить размер на 9x9",
            active_color=(160, 10, 50),
            inactive_color=(230, 230, 230),
            function=lambda: self.__signal_button_select_field(9),
        )
        button_change_field13 = Button(
            position=Position(765, 230),
            size=(230, 70),
            text="Изменить размер на 13x13",
            active_color=(160, 10, 50),
            inactive_color=(230, 230, 230),
            function=lambda: self.__signal_button_select_field(13),
        )
        button_change_field19 = Button(
            position=Position(765, 310),
            size=(230, 70),
            text="Изменить размер на 19x19",
            active_color=(160, 10, 50),
            inactive_color=(230, 230, 230),
            function=lambda: self.__signal_button_select_field(19),
        )
        while True:
            surface.fill((255, 255, 255))
            self._poll_events()
            self.check_click()
            self._computer_move()
            self.draw(surface)
            button_refresh.draw(surface)
            button_exit.draw(surface)
            button_change_field9.draw(surface)
            button_change_field13.draw(surface)
            button_change_field19.draw(surface)
            self._board.check_rules()
            pygame.display.update()
            clock.tick(60)
