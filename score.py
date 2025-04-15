class Score:
    def __init__(self, file_path: str = "scoretable.txt", max_records: int = 10) -> None:
        self.file_name = file_path
        self.table_score: list[int] = []
        self._load_scores()
        self.max_records = max_records

    def _load_scores(self) -> None:
        try:
            with open(self.file_name, "r", encoding="utf-8") as file:
                for line in file:
                    score = line
                    self.table_score.append(int(score))

        except FileNotFoundError:
            pass

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
