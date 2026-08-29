import unittest

from app.services import locket


class LocketParsingTests(unittest.TestCase):
    def test_normalize_username_from_plain_text(self):
        self.assertEqual(locket.normalize_username("alice"), "alice")

    def test_normalize_username_from_locket_url(self):
        self.assertEqual(
            locket.normalize_username("https://locket.cam/alice?utm_source=test"),
            "alice",
        )

    def test_extract_invite_id_from_direct_link(self):
        invite_id = "ABCDEFGHIJKLMNOPQRSTUVWX1234"
        self.assertEqual(
            locket.extract_invite_id(f"https://locket.cam/invites/{invite_id}"),
            invite_id,
        )

    def test_invalid_username_is_rejected_before_network_call(self):
        self.assertFalse(locket.USERNAME_PATTERN.match("bad username with spaces"))


if __name__ == "__main__":
    unittest.main()