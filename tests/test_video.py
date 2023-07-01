import unittest

from pyopenrec.user import User
from pyopenrec.video import Video


class TestVideo(unittest.TestCase):
    v = Video("1o8q43q3yzk")

    def test_yell_rank(self):
        data = self.v.yell_rank()
        self.assertIsNotNone(data)
        self.assertIsInstance(data, list)
        self.assertIsNotNone(data[0]["rank"])
        self.assertIsInstance(data[0]["user"], dict)

    def test_yell_history(self):
        data = self.v.yell_history()
        self.assertIsNotNone(data)
        self.assertIsInstance(data, list)
        self.assertIsNotNone(data[0]["yell"])
        self.assertIsInstance(data[0]["user"], dict)

    def test_get_comments(self):
        comments = self.v.get_comments()
        self.assertIsNotNone(comments)
        self.assertIsInstance(comments, list)
        self.assertIsNotNone(comments[0].id)
        self.assertIsNotNone(comments[0].user)
        self.assertIsInstance(comments[0].user, User)
        self.assertIsNotNone(comments[0].user.id)

    def test_get_recent_comments(self):
        comments = self.v.get_recent_comments()
        self.assertIsNotNone(comments)
        self.assertIsInstance(comments, list)
        self.assertIsNotNone(comments[0].id)
        self.assertIsNotNone(comments[0].user)
        self.assertIsInstance(comments[0].user, User)
        self.assertIsNotNone(comments[0].user.id)

    def test_get_vod_comments(self):
        comments = self.v.get_vod_comments()
        self.assertIsNotNone(comments)
        self.assertIsInstance(comments, list)
        self.assertIsNotNone(comments[0].id)
        self.assertIsNotNone(comments[0].user)
        self.assertIsInstance(comments[0].user, User)
        self.assertIsNotNone(comments[0].user.id)


if __name__ == "__main__":
    unittest.main()
