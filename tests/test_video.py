import unittest

from pyopenrec.video import Video


class TestVideo(unittest.TestCase):
    v = Video()

    def test_stream_list(self):
        data = self.v.stream_list("-total_yells", page=1)
        self.assertEqual(200, data.status)
        self.assertIsNotNone(data.url)
        self.assertIsNotNone(data.data)
        self.assertIsInstance(data.data, list)

    def test_vod_list(self):
        data = self.v.vod_list(sort="created_at", page=2)
        self.assertEqual(200, data.status)
        self.assertIsNotNone(data.url)
        self.assertIsNotNone(data.data)
        self.assertIsInstance(data.data, list)

    def test_movie_list(self):
        data = self.v.movie_list("created_at", page=2)
        self.assertEqual(200, data.status)
        self.assertIsNotNone(data.url)
        self.assertIsNotNone(data.data)
        self.assertIsInstance(data.data, list)

    def test_video_info(self):
        data = self.v.video_info("e5rkej2k1rv")
        self.assertEqual(200, data.status)
        self.assertIsNotNone(data.url)
        self.assertIsNotNone(data.data)
        self.assertIsInstance(data.data, dict)


if __name__ == "__main__":
    unittest.main()
