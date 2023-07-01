import unittest

from pyopenrec import VideoType
from pyopenrec.user import User


class TestUser(unittest.TestCase):
    u = User("indegnasen")

    def test_follows(self):
        followings = self.u.follows()
        self.assertIsNotNone(followings)
        self.assertIsInstance(followings, list)
        self.assertIsInstance(followings[0], User)
        self.assertIsNotNone(followings[0].id)

    def test_followers(self):
        followers = self.u.followers()
        self.assertIsNotNone(followers)
        self.assertIsInstance(followers, list)
        self.assertIsInstance(followers[0], User)
        self.assertIsNotNone(followers[0].id)

    def test_subscription_info(self):
        data = self.u.subscription_info()
        self.assertIsNotNone(data)
        self.assertIsInstance(data, dict)
        self.assertIsNotNone(data["id"])

    def test_contents(self):
        data = self.u.contents(VideoType.vod)
        self.assertIsNotNone(data)
        self.assertIsInstance(data, list)
        self.assertIsNotNone(data[0]["id"])

    def test_captures(self):
        data = self.u.captures()
        self.assertIsNotNone(data)
        self.assertIsInstance(data, list)

    def test_capture_rank(self):
        data = self.u.capture_rank()
        self.assertIsNotNone(data)
        self.assertIsInstance(data, list)

    def test_yell_rank(self):
        data = self.u.yell_rank(month="202101")
        self.assertIsNotNone(data)
        self.assertIsInstance(data, list)


if __name__ == "__main__":
    unittest.main()
