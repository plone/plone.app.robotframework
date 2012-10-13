import unittest

from plone.testing import layered
from plone.app.testing import PLONE_ZSERVER

import robotsuite


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite("acceptance"),
                layer=PLONE_ZSERVER),
    ])
    return suite
