import unittest
import pyopenrec


class TestPlaylist(unittest.TestCase):
    def test_playlists(self):
        data = pyopenrec.playlists("omionna", "capture")
        self.assertEqual(200, data["status"])
        self.assertIsNotNone(data["url"])
        self.assertIsNotNone(data["data"])

    def test_playlist_contents(self):
        data = pyopenrec.playlist_contents("KCug13dxWbk8xaU")
        self.assertEqual(200, data["status"])
        self.assertIsNotNone(data["url"])
        self.assertIsNotNone(data["data"])


if __name__ == "__main__":
    unittest.main()
