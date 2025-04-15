import random
from enum import Enum

import pygame
import pygame.freetype
from pygame import Surface

from board import Board, Position
from game_condition import GameCondition
from idrawable import IDrawable
from widgets.button import Button
from logger import Logger
from score import Score


class GameModes(Enum):
    """Режимы игры"""

    hotseat = 0
    computer_random = 1
    computer_smart = 2


class Game:
    """Главный класс отвечающий за игру"""

    def __init__(self) -> None:
        self._cell_board = 60  # Размер доски
        self._line_width = 2  # Ширина линий поля
        self._initialization_step = 0
        self.condition = GameCondition()
        self.logger = Logger()
        self.logger.info("Create Game")

    def draw(self, surface: Surface) -> None:
        """Отрисовка игрового поля, включая сетку и камни"""

        for x in range(self._board.size):
            pygame.draw.line(
                surface=surface,
                color=(0, 0, 0),
                start_pos=(
                    self._cell_board, self._cell_board + x * self._cell_board
                ),
                end_pos=(
                    self._cell_board + (self._board.size - 1) * self._cell_board,
                    self._cell_board + x * self._cell_board),
                width=self._line_width
            )

            pygame.draw.line(
                surface=surface,
                color=(0, 0, 0),
                start_pos=(
                    self._cell_board + x * self._cell_board, self._cell_board
                ),
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
                    surface.blit(
                        source=self.stone_black,
                        dest=(index_x, index_y)
                    )
                else:
                    surface.blit(
                        source=self.stone_white,
                        dest=(index_x, index_y)
                    )
        self.draw_table(surface)

    def draw_table(self, surface: Surface) -> None:
        """Рисует таблицу рекордов"""

        offset = 150
        count = 1
        text = self.font.render(
            f"Records:",
            True,
            (0, 0, 0),
        )
        surface.blit(
            source=text,
            dest=(770, offset)
        )
        offset += 35
        for scores in self._score.table_score:
            if scores:
                # Тут не поддерживаются именованные аргументы
                text = self.font.render(
                    f"{count} - {scores}",
                    True,
                    (0, 0, 0),
                )
                surface.blit(
                    source=text,
                    dest=(770, offset)
                )
                offset += 35
                count += 1

    def _computer_move(self) -> None:
        """Делает ход за компьютер"""

        if self._move_first_player:
            return

        if self._game_mode == GameModes.hotseat.value:
            return

        while True:
            position = Position(
                random.randint(0, self._board.size - 1),
                random.randint(0, self._board.size - 1),
            )

            if self._make_move(position):
                break

    def _check_click(self) -> None:
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

        if not (
                0 <= current_position.x < self._board.size and
                0 <= current_position.y < self._board.size
        ):
            return

        self._make_move(current_position)

    def _make_move(self, pos: Position) -> bool:
        """Делает ход за текущего игрока"""

        if self._board.check_rock(
                Position(
                    pos.y,
                    pos.x
                )
        ):
            return False

        self._move_first_player = not self._move_first_player
        self._board.add_rock(pos, self._move_first_player + 1)
        if self._move_first_player:
            self._player2_score += 1
        else:
            self._player1_score += 1
        self.logger.info(
            f"The player {int(self._move_first_player) + 1} made a move on the position "
            f"({pos.x}, {pos.y})"
        )
        return True

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
        self._initialization_step = 1
        self.logger.info(f"Field size to {size}x{size}")

    def __signal_button_select_gamemode(self, gamemode: int) -> None:
        """Событие при клике на кнопку"""

        self._game_mode = gamemode
        self._initialization_step = 2
        self.logger.info(f"Gamemode to {gamemode}")

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

    def finish_game(self) -> None:
        """Заканчивает игру, возвращает в главное меню"""

        self.save_score()
        self._board.reset_removed_stones()
        self._initialization_step = 0
        self.refresh()

    def save_score(self) -> None:
        """Сохраняет информацию о результатах игры"""

        removed_stone:tuple[int, int] = self._board.get_tuple_removed_stones()
        self.condition.add_score(stones_removed=removed_stone)
        self.condition.save_scores()

    def exit(self) -> None:
        """Завершает работу приложения"""

        self.finish_game()
        pygame.quit()
        self.logger.info(message="Close Game")
        exit(0)

    def run(self) -> None:
        """Запуск игры"""

        pygame.init()
        self.font = pygame.font.Font(name="assets\Verdana.ttf", size=40)
        self.rock = pygame.image.load(filename="image/rock.png")
        self.monster = pygame.image.load(filename="image/monster.png")
        clock = pygame.time.Clock()
        window_size = (1000, 800)
        surface = pygame.display.set_mode(window_size)

        button_exit = Button(
            position=Position(775, 0),
            size=(70, 70),
            text="Выйти",
            active_color=(160, 10, 50),
            inactive_color=(230, 230, 230),
            function=self.finish_game
        )
        button_field9 = Button(
            position=Position(765, 155),
            size=(230, 70),
            text="Размер поля 9x9",
            active_color=(160, 10, 50),
            inactive_color=(230, 230, 230),
            function=lambda: self.__signal_button_select_field(9)
        )
        button_field13 = Button(
            position=Position(765, 230),
            size=(230, 70),
            text="Размер поля 13x13",
            active_color=(160, 10, 50),
            inactive_color=(230, 230, 230),
            function=lambda: self.__signal_button_select_field(13)
        )
        button_field19 = Button(
            position=Position(765, 310),
            size=(230, 70),
            text="Размер поля 19x19",
            active_color=(160, 10, 50),
            inactive_color=(230, 230, 230),
            function=lambda: self.__signal_button_select_field(19)
        )
        button_gamemode_hotseat = Button(
            position=Position(765, 155),
            size=(230, 70),
            text="Режим игры hotseat",
            active_color=(160, 10, 50),
            inactive_color=(230, 230, 230),
            function=lambda: self.__signal_button_select_gamemode(GameModes.hotseat.value)
        )
        button_gamemode_computer_random = Button(
            position=Position(765, 230),
            size=(230, 70),
            text="Режим игры computer random",
            active_color=(160, 10, 50),
            inactive_color=(230, 230, 230),
            function=lambda: self.__signal_button_select_gamemode(GameModes.computer_random.value)
        )
        button_gamemode_computer_smart = Button(
            position=Position(765, 310),
            size=(230, 70),
            text="Режим игры computer smart",
            active_color=(160, 10, 50),
            inactive_color=(230, 230, 230),
            function=lambda: self.__signal_button_select_gamemode(GameModes.computer_smart.value)
        )
        game_interface_fields_objects: list[IDrawable] = [
            button_field9,
            button_field13,
            button_field19
        ]
        game_interface_gamemodes_objects: list[IDrawable] = [
            button_gamemode_hotseat,
            button_gamemode_computer_random,
            button_gamemode_computer_smart
        ]
        while True:
            surface.fill((255, 255, 255))
            self._poll_events()
            if self._initialization_step == 0:
                for e in game_interface_fields_objects:
                    e.draw(surface)
            elif self._initialization_step == 1:
                for e in game_interface_gamemodes_objects:
                    e.draw(surface)
            elif self._initialization_step == 2:
                self._check_click()
                self._computer_move()
                self.draw(surface)
                button_exit.draw(surface)
                self._board.check_rules()
            pygame.display.update()
            clock.tick(60)
