import unittest

from pyopenrec.playlist import Playlist


class TestPlaylist(unittest.TestCase):
    p = Playlist()

    def test_playlists(self):
        data = self.p.playlists("omionna", "capture")
        self.assertEqual(200, data.status)
        self.assertIsNotNone(data.url)
        self.assertIsNotNone(data.data)
        self.assertIsInstance(data.data, list)

    def test_playlist_contents(self):
        data = self.p.playlist_contents("KCug13dxWbk8xaU")
        self.assertEqual(200, data.status)
        self.assertIsNotNone(data.url)
        self.assertIsNotNone(data.data)
        self.assertIsInstance(data.data, dict)


if __name__ == "__main__":
    unittest.main()
