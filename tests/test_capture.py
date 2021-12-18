import unittest
import pyopenrec


class TestCapture(unittest.TestCase):
    def test_popular_capture(self):
        data = pyopenrec.popular_capture()
        self.assertEqual(200, data["status"])
        self.assertIsNotNone(data["url"])
        self.assertIsNotNone(data["data"])

    def test_capture_list(self):
        data = pyopenrec.capture_list(sort="reaction")
        self.assertEqual(200, data["status"])
        self.assertIsNotNone(data["url"])
        self.assertIsNotNone(data["data"])

    def test_capture_info(self):
        data = pyopenrec.capture_info("72q3gvk0do8")
        self.assertEqual(200, data["status"])
        self.assertIsNotNone(data["url"])
        self.assertIsNotNone(data["data"])


if __name__ == "__main__":
    unittest.main()
