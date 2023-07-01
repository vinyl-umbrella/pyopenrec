import unittest

from pyopenrec.capture import Capture
from pyopenrec.comment import Comment
from pyopenrec.user import User


class TestCapture(unittest.TestCase):
    c = Capture("vjqp0x6rn6y")

    def test_get_comments(self):
        comments = self.c.get_comments()
        self.assertIsNotNone(comments)
        self.assertIsInstance(comments, list)
        self.assertIsInstance(comments[0], Comment)
        self.assertIsNotNone(comments[0].posted_at)
        self.assertIsInstance(comments[0].user, User)
        self.assertIsNotNone(comments[0].user.id)


if __name__ == "__main__":
    unittest.main()
