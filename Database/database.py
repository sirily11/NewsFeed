from typing import List

from Database.logs import Logs
from Database.progress import Progress
from tinydb import TinyDB, Query, where


class DatabaseProvider:
    progress_db: TinyDB
    logs_db: TinyDB

    def __init__(self, feed_id: int = None):
        self.feed_id = feed_id
        self.progress_db = TinyDB('./news_db_progress.json')
        self.logs_db = TinyDB('./log_db.json')
        self.upload_progress_db = TinyDB('./upload_progress.json')

    def update_progress(self, progress: float, is_finished: bool):
        """
        Update current news progress according to the feed_id
        :param is_finished: whether the feed is finished fetching
        :param progress: current progress
        :return:
        """
        pro = Progress(self.feed_id, progress, is_finished)
        self.progress_db.upsert(pro.to_json(), where('news_id') == self.feed_id)

    def update_upload_progress(self, progress: float, is_finished: bool):
        """
        Update current news progress according to the feed_id
        :param is_finished: whether the feed is finished fetching
        :param progress: current progress
        :return:
        """
        pro = Progress(self.feed_id, progress, is_finished)
        self.upload_progress_db.upsert(pro.to_json(), where('news_id') == self.feed_id)

    def add_log(self, msg):
        log = Logs(news_id=self.feed_id, msg=msg)
        self.logs_db.insert(log.to_json())

    def get_progress(self) -> Progress:
        data = self.progress_db.search(where('news_id') == self.feed_id)
        return Progress.from_json(msg=data[0])

    def get_upload_progress(self) -> Progress:
        data = self.upload_progress_db.search(where('news_id') == self.feed_id)
        return Progress.from_json(msg=data[0])

    def get_all_progress(self) -> List[Progress]:
        data = self.progress_db.all()
        return [d for d in data]

    def get_all_upload_progress(self) -> List[Progress]:
        data = self.upload_progress_db.all()
        return [d for d in data]

    def get_logs(self) -> [Logs]:
        data: List = self.logs_db.search(where('news_id') == int(self.feed_id))
        data.reverse()
        return [Logs.from_json(msg=d) for d in data]

    @staticmethod
    def get_all_logs():
        data = TinyDB('./log_db.json').all()
        data.reverse()
        return data


if __name__ == '__main__':
    provider = DatabaseProvider(feed_id=1)
    # provider.add_log("hello")
    print(provider.get_logs())
