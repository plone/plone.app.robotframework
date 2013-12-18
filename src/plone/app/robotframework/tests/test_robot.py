# -*- coding: utf-8 -*-
import unittest

import pkg_resources

try:
    pkg_resources.get_distribution('collective.js.speakjs')
except pkg_resources.DistributionNotFound:
    HAS_SPEAKJS = False
else:
    HAS_SPEAKJS = True

import robotsuite
from plone.app.robotframework.testing import (
    REMOTE_LIBRARY_ROBOT_TESTING,
    SIMPLE_PUBLICATION_ROBOT_TESTING,
    PLONE_ROBOT_TESTING
)
from plone.testing import layered


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite(
                "test_autologin_library.robot"),
                layer=SIMPLE_PUBLICATION_ROBOT_TESTING),
        layered(robotsuite.RobotTestSuite(
                "test_content_library.robot"),
                layer=SIMPLE_PUBLICATION_ROBOT_TESTING),
        layered(robotsuite.RobotTestSuite(
                "test_quickinstaller_library.robot"),
                layer=REMOTE_LIBRARY_ROBOT_TESTING),
        layered(robotsuite.RobotTestSuite(
                "test_i18n_library.robot"),
                layer=PLONE_ROBOT_TESTING),
        layered(robotsuite.RobotTestSuite(
                "test_users_library.robot"),
                layer=PLONE_ROBOT_TESTING),
        layered(robotsuite.RobotTestSuite(
                "docs"),
                layer=PLONE_ROBOT_TESTING),
    ])

    if HAS_SPEAKJS:
        from plone.app.robotframework.testing import SPEAKJS_ROBOT_TESTING

        suite.addTests([
            layered(robotsuite.RobotTestSuite(
                    "test_speakjs_library.robot",
                    noncritical=['non-critical']),
                    layer=SPEAKJS_ROBOT_TESTING),
        ])
    return suite
