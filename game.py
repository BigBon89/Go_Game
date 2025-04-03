import random
from typing import Optional

import pygame
from pygame import Surface

from board import Board
from idrawable import IDrawable
from widgets.button import Button
from widgets.text import Text


class Game:
    """Главный класс отвечающий за игру"""

    def __init__(self) -> None:
        self._game_mode = 0  # 0 - hotseat, 1 - computer random, 2 - computer smart
        self._cell_board = 60  # Размер доски
        self._line_width = 2  # Ширина линий поля
        self._initialization_step = 0
        self._move_first_player = True
        self._board = Board(0)

        self.rock = pygame.image.load('Image/rock.png')
        self.monster = pygame.image.load('Image/monster.png')
        self.FIGURE_SIZE = self._cell_board
        self.stone_black = pygame.transform.scale(self.rock, (self.FIGURE_SIZE, self.FIGURE_SIZE))
        self.stone_white = pygame.transform.scale(self.monster, (self.FIGURE_SIZE, self.FIGURE_SIZE))

    def draw(self, surface: 'Surface') -> None:
        """Отрисовка игрового поля, включая сетку и камни"""

        for i in range(self._board.size):
            pygame.draw.line(surface, (0, 0, 0),
                             (self._cell_board, self._cell_board + i * self._cell_board),
                             (self._cell_board + (self._board.size - 1) * self._cell_board,
                              self._cell_board + i * self._cell_board),
                             self._line_width)
            # Вертикальные линии
            pygame.draw.line(surface, (0, 0, 0),
                             (self._cell_board + i * self._cell_board, self._cell_board),
                             (self._cell_board + i * self._cell_board,
                              self._cell_board + (self._board.size - 1) * self._cell_board),
                             self._line_width)

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

    def exit(self) -> None:
        """Выход из программы"""

        pygame.quit()
        exit(0)

    def _computer_move(self) -> None:
        """Делает ход за компьютер"""

        if self._move_first_player:
            return
        if self._game_mode == 0:
            return

        while True:
            point = (random.randint(0, self._board.size - 1), random.randint(0, self._board.size - 1))
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
        if (min(mouse_pos[0], mouse_pos[1]) < position or max(mouse_pos[0], mouse_pos[1]) >
                position * 2 * self._board.size - 4):
            return

        value = self._cell_board + self._line_width // 2
        coef3 = self._cell_board - self._line_width
        coef1 = mouse_pos[0] - value + coef3 / 2
        coef2 = mouse_pos[1] - value + coef3 / 2
        index_x = int(coef1 / coef3)
        index_y = int(coef2 / coef3)
        if self._board.check_rock(index_y, index_x):
            return
        self._move_first_player = not self._move_first_player
        self._board.add_rock(index_y, index_x, self._move_first_player + 1)

    def _poll_events(self) -> None:
        """Обработка событий окна"""


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass

    def __signal_button_select_field_5(self) -> None:
        """Событие при клике на кнопку"""

        self._board = Board(5)
        self._initialization_step = 2


    def __signal_button_select_field_8(self) -> None:
        """Событие при клике на кнопку"""

        self._board = Board(8)
        self._initialization_step = 2

    def __signal_button_select_field_10(self) -> None:
        """Событие при клике на кнопку"""

        self._board = Board(10)
        self._initialization_step = 2

    def run(self) -> None:
        """Запуск игры"""

        pygame.init()
        clock = pygame.time.Clock()
        window_size = (900, 700)
        surface = pygame.display.set_mode(window_size)
        button = Button((640, 0),
                        (70, 70),
                        "Выйти",
                        (160, 10, 50),
                        (230, 230, 230),
                        exit)
        interface_drawable_interface: list[IDrawable] = []
        interface_drawable_interface.append(Text((100, 100),
                                                 (0, 0, 0),
                                                 "Выберите размер поля",
                                                 16))
        interface_drawable_interface.append(Button((100, 200),
                                                   (100, 100),
                                                   "5",
                                                   (160, 10, 50),
                                                   (230, 230, 230),
                                                   self.__signal_button_select_field_5))
        interface_drawable_interface.append(Button((300, 200),
                                                   (100, 100),
                                                   "8",
                                                   (160, 10, 50),
                                                   (230, 230, 230),
                                                   self.__signal_button_select_field_8))
        interface_drawable_interface.append(Button((500, 200),
                                                   (100, 100),
                                                   "10",
                                                   (160, 10, 50),
                                                   (230, 230, 230),
                                                   self.__signal_button_select_field_10))
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
                button.draw(surface)
                self._board.check_rules()
            pygame.display.update()
            clock.tick(60)
