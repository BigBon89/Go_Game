from typing import Callable, Any

import pygame
from pygame import Surface

from fundamental.clock import Clock
from game.game_state import GameState
from fundamental.score import Score


class GameGraphic:
    def __init__(self,
                 state: GameState,
                 score: Score,
                 filename1: str,
                 filename2: str,
                 global_time: Clock,
                 local_time: Clock,
                 function: [Callable[..., Any]] = None) -> None:
        self.__state = state
        self._score = score
        self._font = pygame.font.Font("assets/Verdana.ttf", 40)
        self._rock = pygame.image.load(filename1)
        self._monster = pygame.image.load(filename2)
        self._global_time = global_time
        self._local_time = local_time
        self.function = function

        self._stone_black: Surface
        self._stone_white: Surface

    def draw(self, surface: Surface) -> None:
        """Отрисовка игрового поля, камней, таблицы рекордов"""

        self._draw_board(surface)
        self._draw_stones(surface)
        self._draw_score_table(surface)
        self._draw_local_time_table(surface)
        self._draw_global_time_table(surface)

    def _draw_board(self, surface: Surface) -> None:
        """Отрисовка игрового поля"""

        for x in range(self.__state.board.size):
            first_y = self.__state.cell_board + x * self.__state.cell_board
            end_x = self.__state.cell_board + (self.__state.board.size - 1) * self.__state.cell_board
            pygame.draw.line(
                surface=surface,
                color=(0, 0, 0),
                start_pos=(self.__state.cell_board, first_y),
                end_pos=(end_x, first_y),
                width=self.__state.line_width
            )

            first_x = self.__state.cell_board + x * self.__state.cell_board
            end_y = self.__state.cell_board + (self.__state.board.size - 1) * self.__state.cell_board
            pygame.draw.line(
                surface=surface,
                color=(0, 0, 0),
                start_pos=(first_x, self.__state.cell_board),
                end_pos=(first_x, end_y),
                width=self.__state.line_width
            )

    def _draw_stones(self, surface: Surface) -> None:
        """Отрисовка камней"""

        self._stone_black = pygame.transform.scale(surface=self._rock,
                                                   size=(self.__state.figure_size, self.__state.figure_size))
        self._stone_white = pygame.transform.scale(surface=self._monster,
                                                   size=(self.__state.figure_size, self.__state.figure_size))

        for x in range(self.__state.board.size):
            for y in range(self.__state.board.size):
                if self.__state.board[x][y] == 0:
                    continue

                index_x = self.__state.cell_board + y * self.__state.cell_board - self.__state.figure_size // 2
                index_y = self.__state.cell_board + x * self.__state.cell_board - self.__state.figure_size // 2
                if self.__state.board[x][y] == 1:
                    pictures = self._stone_black
                else:
                    pictures = self._stone_white
                surface.blit(source=pictures,
                             dest=(index_x, index_y))

    def _draw_score_table(self, surface: Surface) -> None:
        """Отрисовка таблицы рекордов"""

        offset = 150
        text = self._font.render("Records:", True, (0, 0, 0), )
        surface.blit(
            source=text,
            dest=(770, offset)
        )
        offset += 35
        for i, score in enumerate(self._score.table_score, start=1):
            text = self._font.render(f"{i} - {score}", True, (0, 0, 0), )
            surface.blit(
                source=text,
                dest=(770, offset)
            )
            offset += 35

    def _draw_local_time_table(self, surface: Surface):
        """Вырисовка обратного отсчета для таймера"""


        remaining_seconds = self._local_time.reamining_timer()
        timer_text = self._font.render(f"{remaining_seconds} s",
                                       True,
                                       (0, 0, 0)
                                       )
        surface.blit(timer_text, (905, 675))

    def _draw_global_time_table(self, surface: Surface):
        """Время игры"""

        remaining_seconds = self._global_time.reamining_timer()
        timer_text = self._font.render(f"{remaining_seconds // 60} m {remaining_seconds % 60} s",
                                       True,
                                       (0, 0, 0)
                                       )
        surface.blit(timer_text, (790, 725))
        # if self._global_time.is_time_end() and self.function:
        #     self.function()
