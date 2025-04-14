class Score:
    def __init__(self, file_path: str = "scoretable.txt", max_records: int = 10) -> None:
        self.file_name = file_path
        self.__table_score: list[dict[str, int]] = [{} for _ in range(11)]
        self._load_scores()
        self.max_records = max_records

    def _load_scores(self) -> None:
        try:
            with open(self.file_name, "r", encoding="utf-8") as file:
                for line in file:
                    name, score = line.split('-')
                    self.__table_score.append({name: int(score)})

        except FileNotFoundError:
            pass

    def save_scores(self) -> None:
        with open(self.file_name, "w", encoding="utf-8") as file:
            for dictionary in self.__table_score:
                if dictionary:
                    name, score = list(dictionary.items())[0]
                    file.write(f'{name}-{score}\n')

    def add_score(self, name: str, score: int) -> None:
        self.__table_score.append({name: score})
        self.__table_score.sort(key=lambda x: list(x.values()), reverse=True)
        self.__table_score = self.__table_score[:self.max_records]
