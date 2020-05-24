import time
from unittest import TestCase
from Database.database import DatabaseProvider


class DatabaseTest(TestCase):
    def setUp(self):
        self.database = DatabaseProvider(feed_id=1)

    def tearDown(self):
        self.database.db.drop_tables()

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

    def test_remove(self):
        self.database.add_log(msg="New log1")
        self.database.update_progress(40, False)
        self.database.update_upload_progress(30, False)
        p = self.database.get_progress()
        up = self.database.get_upload_progress()
        self.assertEqual(40, p.progress)
        self.assertEqual(30, up.progress)
        self.database.remove_progress()
        self.assertEqual(0, len(self.database.progress_db))
        self.assertEqual(0, len(self.database.upload_progress_db))

