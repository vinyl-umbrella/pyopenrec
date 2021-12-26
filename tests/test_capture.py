import unittest
from pyopenrec.capture import Capture


class TestCapture(unittest.TestCase):
    c = Capture()

    def test_popular_capture(self):
        data = self.c.popular_capture("monthly")
        self.assertEqual(200, data["status"])
        self.assertIsNotNone(data["url"])
        self.assertIsNotNone(data["data"])

    def test_capture_list(self):
        data = self.c.capture_list(sort="reaction")
        self.assertEqual(200, data["status"])
        self.assertIsNotNone(data["url"])
        self.assertIsNotNone(data["data"])

    def test_capture_info(self):
        data = self.c.capture_info("72q3gvk0do8")
        self.assertEqual(200, data["status"])
        self.assertIsNotNone(data["url"])
        self.assertIsNotNone(data["data"])


if __name__ == "__main__":
    unittest.main()
