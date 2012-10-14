import unittest

from plone.testing import layered
from plone.app.testing import PLONE_ZSERVER
from plone.act.tests.layer import POPULATED_PLONEZSERVER

import robotsuite


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite("acceptance"),
                layer=POPULATED_PLONEZSERVER),
    ])
    return suite
