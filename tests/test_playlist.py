import unittest
from pyopenrec.playlist import Playlist


class TestPlaylist(unittest.TestCase):
    def test_playlists(self):
        data = Playlist.playlists("omionna", "capture")
        self.assertEqual(200, data["status"])
        self.assertIsNotNone(data["url"])
        self.assertIsNotNone(data["data"])

    def test_playlist_contents(self):
        data = Playlist.playlist_contents("KCug13dxWbk8xaU")
        self.assertEqual(200, data["status"])
        self.assertIsNotNone(data["url"])
        self.assertIsNotNone(data["data"])


if __name__ == "__main__":
    unittest.main()
