import unittest
from unittest.mock import patch

from app import config


class ConfigHelperTests(unittest.TestCase):
    def test_as_int_uses_default_for_invalid_value(self):
        with patch.dict(config.os.environ, {"EXAMPLE_INT": "not-a-number"}):
            self.assertEqual(config._as_int("EXAMPLE_INT", 7), 7)

    def test_as_bool_accepts_common_true_values(self):
        for value in ("1", "true", "yes", "on", " TRUE "):
            with self.subTest(value=value):
                with patch.dict(config.os.environ, {"EXAMPLE_BOOL": value}):
                    self.assertTrue(config._as_bool("EXAMPLE_BOOL"))

    def test_translation_falls_back_to_key_for_unknown_key(self):
        self.assertEqual(config.T("missing_key", "VI"), "missing_key")

    def test_validate_config_reports_missing_token(self):
        with patch.object(config, "BOT_TOKEN", ""):
            self.assertIn("BOT_TOKEN is required", config.validate_config())


if __name__ == "__main__":
    unittest.main()