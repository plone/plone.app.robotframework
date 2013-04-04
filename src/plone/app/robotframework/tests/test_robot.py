# -*- coding: utf-8 -*-
import os.path
import unittest

import robotsuite
from plone.app.robotframework.testing import (
    REMOTE_LIBRARY_ROBOT_TESTING,
    AUTOLOGIN_ROBOT_TESTING,
    SIMPLE_PUBLICATION_ROBOT_TESTING,
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
                os.path.join("cmfplone", "test_overlays.robot")),
                layer=AUTOLOGIN_ROBOT_TESTING),

        layered(robotsuite.RobotTestSuite(
                os.path.join("cmfplone", "test_actions_menu.robot")),
                layer=SIMPLE_PUBLICATION_ROBOT_TESTING),
        layered(robotsuite.RobotTestSuite(
                os.path.join("cmfplone", "test_edit.robot")),
                layer=AUTOLOGIN_ROBOT_TESTING),
        layered(robotsuite.RobotTestSuite(
                os.path.join("cmfplone", "test_portlets.robot")),
                layer=AUTOLOGIN_ROBOT_TESTING),
        layered(robotsuite.RobotTestSuite(
                os.path.join("cmfplone", "test_history.robot")),
                layer=AUTOLOGIN_ROBOT_TESTING),
        layered(robotsuite.RobotTestSuite(
                os.path.join("cmfplone", "test_folder_contents.robot")),
                layer=AUTOLOGIN_ROBOT_TESTING),
        layered(robotsuite.RobotTestSuite(
                os.path.join("cmfplone", "test_reference_browser.robot")),
                layer=AUTOLOGIN_ROBOT_TESTING),

        layered(robotsuite.RobotTestSuite(
                os.path.join("cmfplone", "test_livesearch.robot")),
                layer=AUTOLOGIN_ROBOT_TESTING),

        layered(robotsuite.RobotTestSuite(
                "test_autologin_library.robot"),
                layer=AUTOLOGIN_ROBOT_TESTING),
        layered(robotsuite.RobotTestSuite(
                "test_quickinstaller_library.robot"),
                layer=REMOTE_LIBRARY_ROBOT_TESTING),
    ])
    return suite
