import unittest
import os.path

from plone.testing import layered
from plone.app.testing import PLONE_ZSERVER
from plone.act.tests.layer import LIVESEARCH_ZSERVER

import robotsuite


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
