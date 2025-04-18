import pygame
from pygame import Surface

from game_state import GameState
from score import Score


class GameGraphic:
    def __init__(self, state: GameState, score: Score, filename1: str, filename2: str) -> None:
        self.state = state
        self.score = score
        self.font = pygame.font.Font("assets/Verdana.ttf", 40)
        self.rock = pygame.image.load(filename1)
        self.monster = pygame.image.load(filename2)

        self.stone_black = None
        self.stone_white = None

    def draw(self, surface: Surface) -> None:
        """Отрисовка игрового поля, камней, таблицы рекордов"""

        self._draw_board(surface)
        self._draw_stones(surface)
        self._draw_score_table(surface)

    def _draw_board(self, surface: Surface) -> None:
        """Отрисовка игрового поля"""

        for x in range(self.state.board.size):
            first_y = self.state.cell_board + x * self.state.cell_board
            end_x = self.state.cell_board + (self.state.board.size - 1) * self.state.cell_board
            pygame.draw.line(
                surface=surface,
                color=(0, 0, 0),
                start_pos=(self.state.cell_board, first_y),
                end_pos=(end_x, first_y),
                width=self.state.line_width
            )

            first_x = self.state.cell_board + x * self.state.cell_board
            end_y = self.state.cell_board + (self.state.board.size - 1) * self.state.cell_board
            pygame.draw.line(
                surface=surface,
                color=(0, 0, 0),
                start_pos=(first_x, self.state.cell_board),
                end_pos=(first_x, end_y),
                width=self.state.line_width
            )

    def _draw_stones(self, surface: Surface) -> None:
        """Отрисовка камней"""

        self.stone_black = pygame.transform.scale(surface=self.rock,
                                                  size=(self.state.figure_size, self.state.figure_size))
        self.stone_white = pygame.transform.scale(surface=self.monster,
                                                  size=(self.state.figure_size, self.state.figure_size))

        for x in range(self.state.board.size):
            for y in range(self.state.board.size):
                if self.state.board[x][y] == 0:
                    continue

                index_x = self.state.cell_board + y * self.state.cell_board - self.state.figure_size // 2
                index_y = self.state.cell_board + x * self.state.cell_board - self.state.figure_size // 2
                if self.state.board[x][y] == 1:
                    pictures = self.stone_black
                else:
                    pictures = self.stone_white
                surface.blit(
                    source=pictures,
                    dest=(index_x, index_y)
                )

    def _draw_score_table(self, surface: Surface) -> None:
        """Отрисовка таблицы рекордов"""

        offset = 150
        # Тут не поддерживаются именованные аргументы
        text = self.font.render("Records:", True, (0, 0, 0), )
        surface.blit(
            source=text,
            dest=(770, offset)
        )
        offset += 35
        for i, score in enumerate(self.score.table_score, start=1):
            text = self.font.render(f"{i} - {score}", True, (0, 0, 0),)
            surface.blit(
                source=text,
                dest=(770, offset)
            )
            offset += 35
