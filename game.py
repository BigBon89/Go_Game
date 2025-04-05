import random
from enum import Enum

import pygame
from pygame import Surface

from board import Board
from idrawable import IDrawable
from widgets.button import Button
from widgets.text import Text
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

        self.rock = pygame.image.load("Image/rock.png")
        self.monster = pygame.image.load("Image/monster.png")
        self.logger = Logger()
        self.logger.info("Create Game")

    def draw(self, surface: "Surface") -> None:
        """Отрисовка игрового поля, включая сетку и камни"""

        for i in range(self._board.size):
            pygame.draw.line(
                surface,
                (0, 0, 0),
                (self._cell_board, self._cell_board + i * self._cell_board),
                (
                    self._cell_board + (self._board.size - 1) * self._cell_board,
                    self._cell_board + i * self._cell_board,
                ),
                self._line_width,
            )

            pygame.draw.line(
                surface,
                (0, 0, 0),
                (self._cell_board + i * self._cell_board, self._cell_board),
                (
                    self._cell_board + i * self._cell_board,
                    self._cell_board + (self._board.size - 1) * self._cell_board,
                ),
                self._line_width,
            )

        for i in range(self._board.size):
            for j in range(self._board.size):
                if self._board[i][j] == 0:
                    continue

                x = self._cell_board + j * self._cell_board - self.FIGURE_SIZE // 2
                y = self._cell_board + i * self._cell_board - self.FIGURE_SIZE // 2

                if self._board[i][j] == 1:
                    surface.blit(self.stone_black, (x, y))
                else:
                    surface.blit(self.stone_white, (x, y))

    def _computer_move(self) -> None:
        """Делает ход за компьютер"""

        if self._move_first_player:
            return
        if self._game_mode == GameModes.hotseat.value:
            return

        while True:
            point = (
                random.randint(0, self._board.size - 1),
                random.randint(0, self._board.size - 1),
            )
            if self._board.check_rock(point[1], point[0]):
                continue
            self._board.game_field[point[0]][point[1]] = 2
            self._move_first_player = not self._move_first_player
            break

    def check_click(self) -> None:
        """Ставит камень при клике на сетку"""

        if not pygame.mouse.get_pressed()[0]:
            return

        if not self._move_first_player and self._game_mode != 0:
            return
        mouse_pos = pygame.mouse.get_pos()
        position = self._cell_board - (self._cell_board - self._line_width) / 2

        if (
            min(mouse_pos[0], mouse_pos[1]) < position
            or max(mouse_pos[0], mouse_pos[1]) >= position * 2 * self._board.size
        ):
            return

        index_x = round((mouse_pos[0] - self._cell_board) / self._cell_board)
        index_y = round((mouse_pos[1] - self._cell_board) / self._cell_board)

        if not (0 <= index_x < self._board.size and 0 <= index_y < self._board.size):
            return

        if self._board.check_rock(index_y, index_x):
            return

        self._move_first_player = not self._move_first_player
        self._board.add_rock(index_y, index_x, self._move_first_player + 1)
        self.logger.info(f"click on field, position {index_x}, {index_y}")

    def _poll_events(self) -> None:
        """Обработка событий окна"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass

    def __signal_button_select_field_9(self) -> None:
        """Событие при клике на кнопку"""

        self._board = Board(9)
        self.characteristics_field(9)
        self.logger.info("Changing the field size to 9x9")

    def __signal_button_select_field_13(self) -> None:
        """Событие при клике на кнопку"""

        self._board = Board(13)
        self.characteristics_field(13)
        self.logger.info("Changing the field size to 13x13")

    def __signal_button_select_field_19(self) -> None:
        """Событие при клике на кнопку"""

        self._board = Board(19)
        self.characteristics_field(19)
        self.logger.info("Changing the field size to 19x19")

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
        for i in range(self._board.size):
            for j in range(self._board.size):
                self._board.add_rock(i, j, 0)
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
            (750, 0),
            (70, 70),
            "Выйти",
            (160, 10, 50),
            (230, 230, 230),
            self.exit
        )
        button_refresh = Button(
            (750, 75),
            (90, 70),
            "Обновить",
            (160, 10, 50),
            (230, 230, 230),
            self.refresh,
        )
        button_change_field9 = Button(
            (750, 155),
            (230, 70),
            "Изменить размер на 9x9",
            (160, 10, 50),
            (230, 230, 230),
            self.__signal_button_select_field_9,
        )
        button_change_field13 = Button(
            (750, 230),
            (230, 70),
            "Изменить размер на 13x13",
            (160, 10, 50),
            (230, 230, 230),
            self.__signal_button_select_field_13,
        )
        button_change_field19 = Button(
            (750, 310),
            (230, 70),
            "Изменить размер на 19x19",
            (160, 10, 50),
            (230, 230, 230),
            self.__signal_button_select_field_19,
        )

        interface_drawable_interface: list[IDrawable] = []
        interface_drawable_interface.append(
            Text((100, 100), (0, 0, 0), "Выберите размер поля", 50)
        )
        interface_drawable_interface.append(
            Button(
                (100, 200),
                (100, 100),
                "9",
                (160, 10, 50),
                (230, 230, 230),
                self.__signal_button_select_field_9,
            )
        )
        interface_drawable_interface.append(
            Button(
                (300, 200),
                (100, 100),
                "13",
                (160, 10, 50),
                (230, 230, 230),
                self.__signal_button_select_field_13,
            )
        )
        interface_drawable_interface.append(
            Button(
                (500, 200),
                (100, 100),
                "19",
                (160, 10, 50),
                (230, 230, 230),
                self.__signal_button_select_field_19,
            )
        )
        while True:
            surface.fill((255, 255, 255))
            self._poll_events()
            if self._initialization_step == 0:
                for e in interface_drawable_interface:
                    e.draw(surface)
            elif self._initialization_step == 1:
                pass
            elif self._initialization_step == 2:
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
