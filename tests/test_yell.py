import unittest
import pyopenrec


class TestYell(unittest.TestCase):
    def test_yell_rank_in_video(self):
        data = pyopenrec.yell_rank_in_video("1o8q43q3yzk")
        self.assertEqual(200, data["status"])
        self.assertIsNotNone(data["url"])
        self.assertIsNotNone(data["data"])

    def test_yell_rank_in_user(self):
        data = pyopenrec.yell_rank_in_user("indegnasen", 202009)
        self.assertEqual(200, data["status"])
        self.assertIsNotNone(data["url"])
        self.assertIsNotNone(data["data"])

    def test_yell_history(self):
        data = pyopenrec.yell_history("1o8q43q3yzk")
        self.assertEqual(200, data["status"])
        self.assertIsNotNone(data["url"])
        self.assertIsNotNone(data["data"])


if __name__ == "__main__":
    unittest.main()