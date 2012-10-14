import unittest

from plone.testing import layered
from plone.act.tests.layer import LIVESEARCH_ZSERVER

import robotsuite


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite("acceptance"),
                layer=LIVESEARCH_ZSERVER),
    ])
    return suite
