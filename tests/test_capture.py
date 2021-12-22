import unittest
from pyopenrec.capture import Capture


class TestCapture(unittest.TestCase):
    def test_popular_capture(self):
        data = Capture.popular_capture("monthly")
        self.assertEqual(200, data["status"])
        self.assertIsNotNone(data["url"])
        self.assertIsNotNone(data["data"])

    def test_capture_list(self):
        data = Capture.capture_list(sort="reaction")
        self.assertEqual(200, data["status"])
        self.assertIsNotNone(data["url"])
        self.assertIsNotNone(data["data"])

    def test_capture_info(self):
        data = Capture.capture_info("72q3gvk0do8")
        self.assertEqual(200, data["status"])
        self.assertIsNotNone(data["url"])
        self.assertIsNotNone(data["data"])


if __name__ == "__main__":
    unittest.main()
