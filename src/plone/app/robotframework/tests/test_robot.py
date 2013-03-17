# -*- coding: utf-8 -*-
import os.path
import unittest

import robotsuite
from plone.app.robotframework.tests._testing import (
    LIVESEARCH_FUNCTIONAL_TESTING,
    REMOTE_LIBRARY_FUNCTIONAL_TESTING,
)
from plone.app.testing import PLONE_ZSERVER
from plone.testing import layered


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite(
                os.path.join("cmfplone", "test_login.robot")),
                layer=PLONE_ZSERVER),
        layered(robotsuite.RobotTestSuite(
                os.path.join("cmfplone", "test_action_menu.robot")),
                layer=PLONE_ZSERVER),
        layered(robotsuite.RobotTestSuite(
                os.path.join("cmfplone", "test_search.robot")),
                layer=LIVESEARCH_FUNCTIONAL_TESTING),
        layered(robotsuite.RobotTestSuite(
                "test_remote_library.robot"),
                layer=REMOTE_LIBRARY_FUNCTIONAL_TESTING),
        layered(robotsuite.RobotTestSuite(
                "test_add_document.robot"),
                layer=PLONE_ZSERVER),
    ])
    return suite
