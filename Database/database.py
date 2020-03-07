import datetime
from typing import List

from Database.logs import Logs
from Database.progress import Progress
from tinydb import TinyDB, Query, where


class DatabaseProvider:
    progress_db: TinyDB
    logs_db: TinyDB

    def __init__(self, feed_id: int = None):
        self.feed_id = feed_id
        self.db = TinyDB('./news_feed.json')
        self.progress_db = self.db.table('progress')
        self.logs_db = self.db.table('logs')
        self.upload_progress_db = self.db.table('upload_progress')

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
        now = datetime.datetime.now()
        log = Logs(news_id=self.feed_id, msg=msg, time=now)
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
        """
        Get all logs according to the feed id
        :return:
        """
        if not self.feed_id:
            raise Exception("You need to define the feed id in order to retrieve this")
        data: List = self.logs_db.search(where('news_id') == int(self.feed_id))
        data.reverse()
        return [Logs.from_json(msg=d) for d in data[:20]]

    def get_all_logs(self):
        """
        Get all logs without using feed id
        :return:
        """
        data = self.logs_db.all()
        data.reverse()
        return data[:30]


if __name__ == '__main__':
    provider = DatabaseProvider(feed_id=1)
    # provider.add_log("hello")
    print(provider.get_logs())
