# -*- coding: utf-8 -*-
import os
import unittest

import robotsuite
from plone.testing import z2
from plone.testing.z2 import FunctionalTesting
from plone.testing import layered

from plone.app.robotframework.testing import PloneRobotFixture


class CustomPloneRobotFixture(PloneRobotFixture):

    def setUp(self):
        os.environ['CONFIGURE_PACKAGES'] = 'plone.session'
        os.environ['APPLY_PROFILES'] = 'plone.session:default'
        super(CustomPloneRobotFixture, self).setUp()

    def tearDown(self):
        super(CustomPloneRobotFixture, self).tearDown()
        if 'CONFIGURE_PACKAGES' in os.environ:
            del os.environ['CONFIGURE_PACKAGES']
        if 'APPLY_PROFILES' in os.environ:
            del os.environ['APPLY_PROFILES']

PLONE_ROBOT_FIXTURE = CustomPloneRobotFixture()

PLONE_ROBOT_TESTING = FunctionalTesting(
    bases=(PLONE_ROBOT_FIXTURE, z2.ZSERVER_FIXTURE),
    name="Plone:Robot"
)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite(
                "test_robotfixture.robot"),
                layer=PLONE_ROBOT_TESTING),
    ])
    return suite
