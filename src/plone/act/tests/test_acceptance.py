import os.path
import unittest

import robotsuite
from plone.act.testing import LIVESEARCH_ZSERVER
from plone.app.testing import PLONE_ZSERVER
from plone.testing import layered


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite(
            os.path.join("acceptance", "standard")),
            layer=PLONE_ZSERVER),
        layered(robotsuite.RobotTestSuite(
            os.path.join("acceptance", "livesearch")),
            layer=LIVESEARCH_ZSERVER),
    ])
    return suite
