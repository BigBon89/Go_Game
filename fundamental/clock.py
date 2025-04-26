import time


class Clock:
    def __init__(self, time_limit: int) -> None:
        self.__turn_time_limit = time_limit
        self.__turn_start_time = time.time()

    def reset_turn_timer(self) -> None:
        """Сброс таймера"""
        self.__turn_start_time = time.time()

    def reamining_timer(self) -> int:
        """Сколько осталось времени на текущий ход"""
        elapsed = time.time() - self.__turn_start_time
        remaining = self.__turn_time_limit - int(elapsed)
        return max(0, remaining)

    def is_time_end(self) -> bool:
        """Проверка, завершилось ли время"""
        return self.reamining_timer() == 0
