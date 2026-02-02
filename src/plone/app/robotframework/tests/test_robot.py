# from plone.app.robotframework.testing import REMOTE_LIBRARY_ROBOT_TESTING
from importlib.metadata import distribution
from importlib.metadata import PackageNotFoundError
from plone.app.robotframework.testing import PLONE_ROBOT_TESTING
from plone.app.robotframework.testing import SIMPLE_PUBLICATION_ROBOT_TESTING
from plone.app.testing import ROBOT_TEST_LEVEL

# from plone.app.robotframework.testing import SIMPLE_PUBLICATION_WITH_TYPES_ROBOT_TESTING
from plone.testing import layered

import robotsuite
import unittest

try:
    distribution("collective.js.speakjs")
    HAS_SPEAKJS = True
except PackageNotFoundError:
    HAS_SPEAKJS = False


ROBOT_TEST_LAYER_MAPPING = [
    ("test_autologin_library.robot", SIMPLE_PUBLICATION_ROBOT_TESTING),
    ("test_content_library.robot", SIMPLE_PUBLICATION_ROBOT_TESTING),
    ("test_quickinstaller_library.robot", SIMPLE_PUBLICATION_ROBOT_TESTING),
    ("test_i18n_library.robot", SIMPLE_PUBLICATION_ROBOT_TESTING),
    ("test_users_library.robot", PLONE_ROBOT_TESTING),
    ("docs", PLONE_ROBOT_TESTING),
]


def test_suite():

    suite = unittest.TestSuite()

    for robot_test, test_layer in ROBOT_TEST_LAYER_MAPPING:
        robottestsuite = robotsuite.RobotTestSuite(
            robot_test,
            noncritical=["unstable"],
        )
        robottestsuite.level = ROBOT_TEST_LEVEL
        suite.addTests(
            [
                layered(robottestsuite, layer=test_layer),
            ]
        )

    if HAS_SPEAKJS:
        from plone.app.robotframework.testing import SPEAKJS_ROBOT_TESTING

        robottestsuite = robotsuite.RobotTestSuite(
            "test_speakjs_library.robot",
            noncritical=["non-critical"],
        )
        robottestsuite.level = ROBOT_TEST_LEVEL
        suite.addTests(
            [
                layered(
                    robottestsuite,
                    layer=SPEAKJS_ROBOT_TESTING,
                ),
            ]
        )

    return suite
