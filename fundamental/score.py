from pathlib import Path

from fundamental.logger import Logger


class Score:
    DEFAULT_FILE_PATH = Path("scoretable.txt")
    MAX_RECORDS = 10

    def __init__(self, logger: Logger, max_records: int = MAX_RECORDS, file_path: Path = DEFAULT_FILE_PATH) -> None:
        self._logger = logger
        self.file_name = file_path
        self.table_score: list[int] = []
        self._load_scores()
        self.max_records = max_records

    def _load_scores(self) -> None:
        try:
            with open(self.file_name, "r", encoding="utf-8") as file:
                for line in file:
                    self.table_score.append(int(line))

        except FileNotFoundError:
            self._logger.info("Файл с рекордами не найден")

    def save_scores(self) -> None:
        with open(self.file_name, "w", encoding="utf-8") as file:
            for element in self.table_score:
                if element:
                    score = element
                    file.write(f'{score}\n')

    def add_score(self, score: int) -> None:
        self.table_score.append(score)
        self.table_score.sort(reverse=True)
        self.table_score = self.table_score[:self.max_records]
