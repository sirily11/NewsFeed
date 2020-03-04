from Database.encodeable import Encodeable


class Progress(Encodeable):
    @staticmethod
    def from_json(msg: dict):
        return Progress(
            news_id=msg['news_id'],
            progress=msg['progress'],
            is_finished=msg['is_finished']
        )

    def to_json(self) -> dict:
        return {
            "news_id": self.news_id,
            "progress": self.progress,
            'is_finished': self.is_finished
        }

    def __init__(self, news_id, progress: float, is_finished: bool):
        self.news_id = news_id
        self.progress = progress
        self.is_finished = is_finished

    def __str__(self):
        return f'{self.news_id} - {self.progress}'
