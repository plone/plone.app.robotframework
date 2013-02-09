import unittest

import robotsuite
from plone.act.testing import REMOTE_LIBRARY_FUNCTIONAL_TESTING
from plone.testing import layered


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite("robot_remote.txt"),
                layer=REMOTE_LIBRARY_FUNCTIONAL_TESTING),
    ])
    return suite
