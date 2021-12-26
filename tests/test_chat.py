import unittest
from pyopenrec.chat import Chat
from pyopenrec.video import Video


class TestChat(unittest.TestCase):
    c = Chat()
    v = Video()

    def test_get_comment(self):
        v = self.v.stream_list()
        vid = v["data"][0]["id"]
        ws = self.c.get_ws(vid)
        self.assertTrue((ws.startswith("wss://")))


if __name__ == "__main__":
    unittest.main()
