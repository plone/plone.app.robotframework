Writing Robot Framework tests with plone.app.robotframework
===========================================================

**plone.app.robotframework** provides `Robot Framework
<http://code.google.com/p/robotframework/>`_ compatible resources and tools for
writing functional Selenium tests (including acceptance tests) for Plone CMS
and its add-ons.


Require plone.app.robotframework
--------------------------------

Update ``setup.py`` to require *plone.app.robotframework*:

.. code-block:: python

   extras_require={
       'test': [
           ...
           'plone.app.robotframework',
       ],
   },

All you need is *plone.app.robotframework*, because it will require the rest
(*selenium*, *robotframework*, robotframework-selenium2library* and
*robotsuite*).

.. note:: Selenium-bindings for Python use Firefox as the default browser.
   Unless you know how to configure other browsers to work with Selenium you
   should have Firefox installed in your system


Define functional testing layer
-------------------------------

Plone add-on testing requires defining test layers,
which setup Plone, the add-ons and any custom configuration
required by the tests.

Update your ``src/my/product/testing.py`` to include:

.. code-block:: python

   from plone.testing import z2
   from plone.app.testing import FunctionalTesting
   from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE

   MY_PRODUCT_ROBOT_TESTING = FunctionalTesting(
      bases=(MY_PRODUCT_FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE,
             z2.ZSERVER_FIXTURE),
       name="MyProduct:Robot")

.. note:: AUTOLOGIN_LIBRARY_FIXTURE is optional, but it will allow you to
   write faster Selenium tests, because tests don't need to spend time on
   login forms. Also note that the order of the bases matters.

If you don't have any testing layers for your product yet, or want to know
more about them, please read: http://pypi.python.org/pypi/plone.app.testing


Install Robot-tools
-------------------

*plone.app.robotframework* ships with two main helper scripts for
writing tests:

* ``bin/robot-server`` starts a temporary Plone site with the given
  test layer set up

* ``bin/robot`` executes Robot Framework's ``pybot``-runner so that it
  will run the given test suite agains the running ``robot-server``,
  ensuring that tests will be run in isolation (database is cleaned between
  the tests)

Update ``buildout.cfg``:

.. code-block:: ini

   [buildout]
   parts =
       ...
       robot

   [robot]
   recipe = zc.recipe.egg
   eggs =
       Pillow
       ${test:eggs}
       plone.app.robotframework

.. note:: Robot-tools are optional, but will ease and speed up your test
   development.


Start test server
-----------------

Once the buildout with Robot-tools is run, start the test server with:

.. code-block:: bash

    $ bin/robot-server my.product.testing.MY_PRODUCT_ROBOT_TESTING

Once the test server has started, there's a test Plone-site served
at http://localhost:55001/plone/ (by default).


Write the first test
--------------------

Robot tests are written in test suites, which are plain text files, usually
ending with ``.robot`` (and older ones with ``.txt``).

The first test can be written anywhere in the filesystem.

For example, a ``test_hello.robot``:

.. code-block:: robotframework

   *** Settings ***

   Resource  plone/app/robotframework/selenium.robot

   Test Setup  Open test browser
   Test Teardown  Close all browsers

   *** Test Cases ***

   Plone is installed
       Go to  ${PLONE_URL}
       Page should contain  Powered by Plone

Robot is all about running test clauses called **keywords** (or, to be more
exact, keyword calls with parameters). Every test case may contain one or more
keywords, which are run sequentially -- usually until the first of them fails.

Keywords are defined in **keyword libraries** and as **user keywords**. Keyword
libraries can be Python libraries or XML-RPC-services. User keywords are lists
of test clauses reusing existing keywords or other user keywords.

Here is a more complicated example with some user keywords in action:

.. code:: robotframework

   *** Settings ***

   Resource  plone/app/robotframework/selenium.robot

   Library  Remote  ${PLONE_URL}/RobotRemote

   Test Setup  Open test browser
   Test Teardown  Close all browsers

   *** Test Cases ***

   Site Administrator can access control panel
       Given I'm logged in as a 'Site Administrator'
        When I open the personal menu
        Then I see the Site Setup -link

   *** Keywords ***

   I'm logged in as a '${ROLE}'
       Enable autologin as  ${ROLE}
       Go to  ${PLONE_URL}

   I open the personal menu
       Click link  css=#user-name

   I see the Site Setup -link
       Element should be visible  css=#personaltools-plone_setup

.. note:: We use ``.robot`` as the Robot Framework test suite file extension
   to make it easier for developers to configure Robot Framework syntax
   highlighting for their editors (otherwise ``.txt`` would work also).


Run the first test
------------------

Once the ``bin/robot-server`` has been started and a test suite has been
written, the new test suite can be run with ``bin/robot``:

.. code-block:: bash

   $ bin/robot test_hello.robot

.. note:: ``bin/robot`` is mostly just a wrapper for Robot Framework's
   pybot test runner, but it does inject necessary options to enable
   plone.testing's test isolation for Plone when used together with
   ``bin/robot-server``.


Integrate with Zope-testrunner
------------------------------

Because it's convenient to run Robot tests with other *zope.testrunner*
tests (e.g. on Jenkins or Travis-CI), we usually want to integrate
Robot tests to be run with other tests using *zope.testrunner*.

For *zope.testrunner* integration, create
``src/my/product/tests/test_robot.py``:

.. code-block:: python

   import unittest

   import robotsuite
   from my.product.testing import MY_PRODUCT_ROBOT_TESTING
   from plone.testing import layered


   def test_suite():
       suite = unittest.TestSuite()
       suite.addTests([
           layered(robotsuite.RobotTestSuite('test_hello.robot'),
                   layer=MY_PRODUCT_ROBOT_TESTING),
       ])
       return suite

.. note:: For this to work and ``zope.testrunner`` to discover your
   robot test suite, remember to move ``test_hello.robot`` under
   ``my/product/tests``.

`RobotSuite <http://pypi.python.org/pypi/robotsuite/>`_ is our package for
wrapping Robot Framework tests into Python unittest compatible test cases.
It's good to know that this registration pattern is the same as how
doctest-suites are registered to support zope.testrunner's layers (see
https://pypi.python.org/pypi/plone.testing for layered doctest examples).


Running tests with zope.testrunner
----------------------------------

Once your robot test have been integrated with *zope.testrunner* using
``test_robot.py``-module (or any other module returning RobotTestSuite),
you can list your integrated robot test cases with command:

.. code:: bash

   $ bin/test --list-tests

And run robot tests cases with all other test cases with command:

.. code:: bash

   $ bin/test

You can filter robot test normally using ``-t``-argument for
*zope.testrunnner*:

.. code:: bash

   $ bin/test -t robot

And it's also possible to filter test by tags:

.. code::

   $ bin/test -t \#mytag

Or exclude them:

.. code::

   $ bin/test -t \!robot


How to write more tests
-----------------------

The most difficult part in writing robot tests with Selenium-keywords is to know
the application you are testing: which link to click when and to which field to
input test data.

Robot Framework ships with a few selected standard libraries. One of them is
the *Dialogs*-library, which provides a very useful keyword: *Pause execution*.
By importing Dialogs-library (while developing the test) and adding the *Pause
execution* keyword, you can pause the test at any point to make it possible to
figure out what to do next.
(Dialogs depend on `TkInter-library <http://wiki.python.org/moin/TkInter>`_.)

For example::

    *** Settings ***

    Resource  plone/app/robotframework/selenium.robot
    Resource  plone/app/robotframework/saucelabs.robot

    Library  Remote  ${PLONE_URL}/RobotRemote

    Test Setup  Open SauceLabs test browser
    Test Teardown  Run keywords  Report test status  Close all browsers

    *** Test Cases ***

    Plomino is installed
        Go to  ${PLONE_URL}
        Pages should contain  mydb

    Let me think what to do next
        Enable autologin as  Site Administrator
        Go to  ${PLONE_URL}
        Import library  Dialogs
        Pause execution

.. note:: Be sure to remove the Dialogs-library import and its keywords
   before commit, because Dialogs-library may have dependencies,
   which are not available on your CI-machine.


Resources
---------

- http://robotframework.googlecode.com/hg/doc/libraries/BuiltIn.html?r=2.7.7
- http://rtomac.github.com/robotframework-selenium2library/doc/Selenium2Library.html
- http://code.google.com/p/robotframework/wiki/HowToWriteGoodTestCases
- http://code.google.com/p/robotframework/


Examples:
---------

- https://github.com/plone/plone.app.robotframework/tree/master/src/plone/app/robotframework/tests
- http://plone.293351.n2.nabble.com/Robot-Framework-How-to-fill-TinyMCE-s-text-field-tp7563662p7563691.html
