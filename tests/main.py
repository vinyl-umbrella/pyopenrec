import unittest

import test_capture
import test_channel
import test_comment
import test_playlist
import test_video
import test_yell


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(test_capture.TestCapture))
    suite.addTest(unittest.makeSuite(test_channel.TestChannel))
    suite.addTest(unittest.makeSuite(test_comment.TestComment))
    suite.addTest(unittest.makeSuite(test_playlist.TestPlaylist))
    suite.addTest(unittest.makeSuite(test_video.TestVideo))
    suite.addTest(unittest.makeSuite(test_yell.TestYell))
    return suite


if __name__ == '__main__':
    mySuite = suite()
    unittest.TextTestRunner().run(mySuite)
