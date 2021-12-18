import unittest
import pyopenrec


class TestVideo(unittest.TestCase):
    def test_stream_list(self):
        data = pyopenrec.stream_list("-total_yells", page=1)
        self.assertEqual(200, data["status"])
        self.assertIsNotNone(data["url"])
        self.assertIsNotNone(data["data"])

    def test_vod_list(self):
        data = pyopenrec.vod_list(page=2)
        self.assertEqual(200, data["status"])
        self.assertIsNotNone(data["url"])
        self.assertIsNotNone(data["data"])

    def test_movie_list(self):
        data = pyopenrec.movie_list("created_at", page=2)
        self.assertEqual(200, data["status"])
        self.assertIsNotNone(data["url"])
        self.assertIsNotNone(data["data"])

    def test_video_info(self):
        data = pyopenrec.video_info("e5rkej2k1rv")
        self.assertEqual(200, data["status"])
        self.assertIsNotNone(data["url"])
        self.assertIsNotNone(data["data"])


if __name__ == "__main__":
    unittest.main()
