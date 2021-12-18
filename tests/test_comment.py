import unittest
import pyopenrec


class TestComment(unittest.TestCase):
    def test_get_comment(self):
        data = pyopenrec.get_comment(
            "n9ze3m2w184", "2021-12-18T17:30:33+09:00")
        self.assertEqual(200, data["status"])
        self.assertIsNotNone(data["url"])
        self.assertIsNotNone(data["data"])

    def test_get_recent_comment(self):
        data = pyopenrec.get_recent_comment("n9ze3m2w184")
        self.assertEqual(200, data["status"])
        self.assertIsNotNone(data["url"])
        self.assertIsNotNone(data["data"])

    def test_get_vod_comment(self):
        data = pyopenrec.get_vod_comment("e2zw69jmw8o")
        self.assertEqual(200, data["status"])
        self.assertIsNotNone(data["url"])
        self.assertIsNotNone(data["data"])


# j = pyopenrec.post_comment("kdr7x6y5w8j", "test", credentials["data"])
# j = pyopenrec.post_vod_comment("n9ze3n30184", "test", credentials["data"])
# j = pyopenrec.reply_vod_comment("e2zw69jmw8o", 140103, "test", credentials["data"])


if __name__ == "__main__":
    unittest.main()
