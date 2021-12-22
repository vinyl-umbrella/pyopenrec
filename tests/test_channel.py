import unittest
from pyopenrec.channel import Channel
from pyopenrec.video import Video


class TestChannel(unittest.TestCase):
    def test_channel_rank(self):
        data = Channel.channel_rank("monthly", date=201912)
        self.assertEqual(200, data["status"])
        self.assertIsNotNone(data["url"])
        self.assertIsNotNone(data["data"])

    def test_channel_info(self):
        data = Channel.channel_info("sumomo_xqx")
        self.assertEqual(200, data["status"])
        self.assertIsNotNone(data["url"])
        self.assertIsNotNone(data["data"])

    def test_subscription_info(self):
        data = Channel.subscription_info("indegnasen")
        self.assertEqual(200, data["status"])
        self.assertIsNotNone(data["url"])
        self.assertIsNotNone(data["data"])

    def test_is_streaming(self):
        v = Video.stream_list()
        user_id = v["data"][0]["channel"]["id"]
        b = Channel.is_streaming(user_id)
        self.assertTrue(b)


if __name__ == "__main__":
    unittest.main()
