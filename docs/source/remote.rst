Speed up your BDD Given-clauses via a remote library
====================================================

BDD-style tests begin with one or more *Given*-clauses that should setup the
test environment for the actual tests-clauses (*When* and *Then*).

Because Given-clauses are not really part of the actual test, it is not
necessary to run them through Selenium (using Selenium2Library), but it would
be faster to write custon Python keywords for them.

**plone.act** includes an example, how to a robot
`remote library <http://robotframework.googlecode.com/hg/doc/userguide/RobotFrameworkUserGuide.html?r=2.7.6#remote-library-interface>`_,
which could be called to interact with the site without Selenium.

The base implementation is provided at:

    https://github.com/plone/plone.app.robotframework/blob/master/src/plone/app/robotframework/remote.py

    https://github.com/plone/plone.app.robotframework/blob/master/src/plone/app/robotframework/quickinstaller.py

An example integration into testing layer is provided at:

    https://github.com/plone/plone.app.robotframework/blob/master/src/plone/app/robotframework/testing.py#L65

An example test suite using the library is provided at:

    https://github.com/plone/plone.app.robotframework/blob/master/src/plone/app/robotframework/tests/test_robot.py#L48

    https://github.com/plone/plone.app.robotframework/blob/master/src/plone/app/robotframework/tests/robot_quickinstaller_library.robot
