import tempfile
import unittest
from pathlib import Path

from app import database


class DatabaseHelperTests(unittest.TestCase):
    def setUp(self):
        self._original_db_path = database.DB_PATH
        self._tmp = tempfile.TemporaryDirectory()
        database.DB_PATH = Path(self._tmp.name) / "test_bot.db"
        database.init_db()

    def tearDown(self):
        database.DB_PATH = self._original_db_path
        self._tmp.cleanup()

    def test_usage_counter_starts_at_zero_and_increments(self):
        user_id = 1001
        self.assertEqual(database.get_user_usage(user_id), 0)
        database.increment_usage(user_id)
        self.assertEqual(database.get_user_usage(user_id), 1)

    def test_language_setting_round_trip(self):
        user_id = 1002
        database.set_lang(user_id, "EN")
        self.assertEqual(database.get_lang(user_id), "EN")

    def test_config_setting_round_trip(self):
        database.set_config("sample", "value")
        self.assertEqual(database.get_config("sample"), "value")

    def test_stats_include_logged_request(self):
        database.log_request(1003, "invite-id", "SUCCESS")
        stats = database.get_stats()
        self.assertEqual(stats["total"], 1)
        self.assertEqual(stats["success"], 1)
        self.assertEqual(stats["fail"], 0)


if __name__ == "__main__":
    unittest.main()