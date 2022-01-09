import unittest
from datetime import datetime
from pyopenrec.comment import Comment


class TestComment(unittest.TestCase):
    c = Comment()

    def test_get_comment(self):
        dt = datetime(2021, 12, 21, 0, 0, 0)
        data = self.c.get_comment("n9ze3m2w184", dt)
        self.assertEqual(200, data["status"])
        self.assertIsNotNone(data["url"])
        self.assertIsNotNone(data["data"])
        self.assertIsInstance(data["data"], list)

    def test_get_recent_comment(self):
        data = self.c.get_recent_comment("n9ze3m2w184")
        self.assertEqual(200, data["status"])
        self.assertIsNotNone(data["url"])
        self.assertIsNotNone(data["data"])
        self.assertIsInstance(data["data"], list)

    def test_get_vod_comment(self):
        data = self.c.get_vod_comment("e2zw69jmw8o")
        self.assertEqual(200, data["status"])
        self.assertIsNotNone(data["url"])
        self.assertIsNotNone(data["data"])
        self.assertIsInstance(data["data"], list)


if __name__ == "__main__":
    unittest.main()
