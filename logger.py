import logging


class Logger:
    def __init__(self, log_file: str="logger.log", level:int =logging.INFO) -> None:
        self.logger = logging.getLogger("logs for Go_Game")
        self.logger.setLevel(level)

        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def debug(self, message: str) -> None:
        """Логирования для отладочной информации"""

        self.logger.debug(message)

    def info(self, message: str) -> None:
        """Логирования для каких-то информационных сообщений"""

        self.logger.info(message)