from Database.encodeable import Encodeable
import datetime


class Logs(Encodeable):
    @staticmethod
    def from_json(msg):
        return Logs(news_id=msg['news_id'],
                    msg=msg['message'],
                    time=msg['time'])

    def to_json(self) -> dict:
        return {"news_id": self.news_id, "message": self.msg, 'time': str(datetime.datetime.now())}

    def __init__(self, news_id, msg: str, time=datetime.datetime.now()):
        self.news_id = news_id
        self.msg = msg
        self.time = time

    def __str__(self):
        return self.msg
