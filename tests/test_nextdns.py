import asyncio
import unittest

from app.services import nextdns


class NextDnsTests(unittest.TestCase):
    def test_create_profile_without_api_key_returns_empty_result(self):
        logs: list[str] = []
        profile_id, link = asyncio.run(nextdns.create_profile("", ["example.com"], logs.append))

        self.assertIsNone(profile_id)
        self.assertIsNone(link)
        self.assertIn("NEXTDNS_KEY is not configured.", logs)


if __name__ == "__main__":
    unittest.main()