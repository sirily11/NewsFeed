import time
from unittest import TestCase
from Database.database import DatabaseProvider


class DatabaseTest(TestCase):
    def setUp(self):
        self.database = DatabaseProvider(feed_id=1)

    def tearDown(self):
        self.database.db.purge_tables()

    def test_add_logs(self):
        self.database.add_log(msg="New log1")
        self.database.add_log(msg="New log2")
        logs = self.database.get_logs()
        self.assertEqual(2, len(logs))

    def test_add_logs_time(self):
        self.database.add_log(msg="New log1")
        time.sleep(1)
        self.database.add_log(msg="New log2")
        logs = self.database.get_logs()
        # Two logs should not with same time
        self.assertNotEqual(logs[0].time, logs[1].time)

