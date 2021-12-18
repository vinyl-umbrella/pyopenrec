import unittest
import pyopenrec


class TestChannel(unittest.TestCase):
    def test_channel_rank(self):
        data = pyopenrec.channel_rank("monthly", date=201912)
        self.assertEqual(200, data["status"])
        self.assertIsNotNone(data["url"])
        self.assertIsNotNone(data["data"])

    def test_channel_info(self):
        data = pyopenrec.channel_info("sumomo_xqx")
        self.assertEqual(200, data["status"])
        self.assertIsNotNone(data["url"])
        self.assertIsNotNone(data["data"])

    def test_subscription_info(self):
        data = pyopenrec.subscription_info("indegnasen")
        self.assertEqual(200, data["status"])
        self.assertIsNotNone(data["url"])
        self.assertIsNotNone(data["data"])


if __name__ == "__main__":
    unittest.main()
