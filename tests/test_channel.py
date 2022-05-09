import unittest

from pyopenrec.channel import Channel
from pyopenrec.video import Video


class TestChannel(unittest.TestCase):
    c = Channel()
    v = Video()

    def test_channel_rank(self):
        data = self.c.channel_rank("monthly", date=201912)
        self.assertEqual(200, data.status)
        self.assertIsNotNone(data.url)
        self.assertIsNotNone(data.data)
        self.assertIsInstance(data.data, list)

    def test_channel_info(self):
        data = self.c.channel_info("sumomo_xqx")
        self.assertEqual(200, data.status)
        self.assertIsNotNone(data.url)
        self.assertIsNotNone(data.data)
        self.assertIsInstance(data.data, dict)

    def test_subscription_info(self):
        data = self.c.subscription_info("indegnasen")
        self.assertEqual(200, data.status)
        self.assertIsNotNone(data.url)
        self.assertIsNotNone(data.data)
        self.assertIsInstance(data.data, dict)

    def test_contents(self):
        data = self.c.contents("indegnasen", 2, page=2)
        self.assertEqual(200, data.status)
        self.assertIsNotNone(data.url)
        self.assertIsNotNone(data.data)
        self.assertIsInstance(data.data, list)

    def test_get_follow(self):
        data = self.c.get_follow("indegnasen")
        self.assertEqual(200, data.status)
        self.assertIsNotNone(data.url)
        self.assertIsNotNone(data.data)
        self.assertIsInstance(data.data, list)

    def test_get_follower(self):
        data = self.c.get_follower("indegnasen")
        self.assertEqual(200, data.status)
        self.assertIsNotNone(data.url)
        self.assertIsNotNone(data.data)

    def test_is_streaming(self):
        v = self.v.stream_list()
        user_id = v.data[0]["channel"]["id"]
        b = self.c.is_streaming(user_id)
        self.assertTrue(b)


if __name__ == "__main__":
    unittest.main()
