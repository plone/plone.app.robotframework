from plone.app.robotframework.testing import PloneRobotFixture
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.testing import layered
from plone.testing.zope import FunctionalTesting
from plone.testing.zope import WSGI_SERVER_FIXTURE

import os
import robotsuite
import unittest


class CustomPloneRobotFixture(PloneRobotFixture):
    def setUp(self):
        os.environ["CONFIGURE_PACKAGES"] = "plone.session"
        os.environ["APPLY_PROFILES"] = "plone.session:default"
        super().setUp()

    def tearDown(self):
        super().tearDown()
        if "CONFIGURE_PACKAGES" in os.environ:
            del os.environ["CONFIGURE_PACKAGES"]
        if "APPLY_PROFILES" in os.environ:
            del os.environ["APPLY_PROFILES"]


PLONE_ROBOT_FIXTURE = CustomPloneRobotFixture()

PLONE_ROBOT_TESTING = FunctionalTesting(
    bases=(
        PLONE_ROBOT_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        WSGI_SERVER_FIXTURE,
    ),
    name="Plone:Robot",
)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests(
        [
            layered(
                robotsuite.RobotTestSuite("test_robotfixture.robot"),
                layer=PLONE_ROBOT_TESTING,
            ),
        ]
    )
    return suite
