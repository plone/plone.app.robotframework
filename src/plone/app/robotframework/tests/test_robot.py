# from plone.app.robotframework.testing import REMOTE_LIBRARY_ROBOT_TESTING
from importlib.metadata import distribution
from importlib.metadata import PackageNotFoundError
from plone.app.robotframework.testing import PLONE_ROBOT_TESTING
from plone.app.robotframework.testing import SIMPLE_PUBLICATION_ROBOT_TESTING

# from plone.app.robotframework.testing import SIMPLE_PUBLICATION_WITH_TYPES_ROBOT_TESTING
from plone.testing import layered

import robotsuite
import unittest


try:
    distribution("collective.js.speakjs")
    HAS_SPEAKJS = True
except PackageNotFoundError:
    HAS_SPEAKJS = False


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests(
        [
            layered(
                robotsuite.RobotTestSuite("test_browser_library.robot"),
                layer=SIMPLE_PUBLICATION_ROBOT_TESTING,
            ),
            layered(
                robotsuite.RobotTestSuite("test_autologin_library.robot"),
                layer=SIMPLE_PUBLICATION_ROBOT_TESTING,
            ),
            layered(
                robotsuite.RobotTestSuite("test_content_library.robot"),
                layer=SIMPLE_PUBLICATION_ROBOT_TESTING,
            ),
            # layered(
            #     robotsuite.RobotTestSuite("test_quickinstaller_library.robot"),
            #     layer=REMOTE_LIBRARY_ROBOT_TESTING,
            # ),
            layered(
                robotsuite.RobotTestSuite("test_i18n_library.robot"),
                layer=PLONE_ROBOT_TESTING,
            ),
            layered(
                robotsuite.RobotTestSuite("test_users_library.robot"),
                layer=PLONE_ROBOT_TESTING,
            ),
            layered(robotsuite.RobotTestSuite("docs"), layer=PLONE_ROBOT_TESTING),
        ]
    )

    if HAS_SPEAKJS:
        from plone.app.robotframework.testing import SPEAKJS_ROBOT_TESTING

        suite.addTests(
            [
                layered(
                    robotsuite.RobotTestSuite(
                        "test_speakjs_library.robot",
                        noncritical=["non-critical"],
                    ),
                    layer=SPEAKJS_ROBOT_TESTING,
                )
            ]
        )
    return suite
