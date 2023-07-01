import unittest

import test_capture
import test_user
import test_video


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(test_capture.TestCapture))
    suite.addTest(unittest.makeSuite(test_video.TestVideo))
    suite.addTest(unittest.makeSuite(test_user.TestUser))
    return suite


if __name__ == "__main__":
    mySuite = suite()
    unittest.TextTestRunner().run(mySuite)
