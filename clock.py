import time


class Clock:
    def __init__(self, time_limit: int):
        self.turn_time_limit = time_limit
        self.turn_start_time = time.time()

    def reset_turn_timer(self):
        self.turn_start_time = time.time()

    def reamining_timer(self):
        """Сколько осталось времени на текущий ход"""
        elapsed = time.time() - self.turn_start_time
        remaining = self.turn_time_limit - int(elapsed)
        return max(0, remaining)

    def is_time_end(self):
        return self.reamining_timer() == 0