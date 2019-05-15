How to write Robot Framework tests for Plone
============================================

This is a brief tutorial for writing Robot Framework test for Plone with
`plone.app.robotframework`_. *plone.app.robotframework* provides `Robot
Framework`_ -compatible resources and tools for writing functional Selenium
tests (including acceptance tests) for Plone CMS and its add-ons. (See also
:doc:`examples` for more ideas).

.. _plone.app.robotframework: http://pypi.python.org/pypi/plone.app.robotframework


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

All you need is *plone.app.robotframework*. It will require the rest
(selenium_, robotframework_, `robotframework-selenium2library`_ and
also robotsuite_).

.. note:: Selenium-bindings for Python use Firefox as the default browser.
   Unless you know how to configure other browsers to work with Selenium you
   should have Firefox installed in your system

.. _Robot Framework: http://robotframework.org
.. _selenium: http://pypi.python.org/pypi/selenium
.. _robotframework: http://pypi.python.org/pypi/robotframework
.. _robotframework-selenium2library: http://pypi.python.org/pypi/robotframework-selenium2library
.. _robotsuite: http://pypi.python.org/pypi/robotsuite


Define functional testing layer
-------------------------------

Plone add-on testing requires defining a custom test layer,
which setups Plone-sandbox, the dependent add-ons and any custom configuration
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
more about them, please read `plone.app.testing`_-documentation.

.. _plone.app.testing: http://pypi.python.org/pypi/plone.app.testing


Install Robot-tools
-------------------

*plone.app.robotframework* ships with two main helper scripts for
writing tests:

* ``bin/robot-server`` starts a temporary Plone site with the given
  test layer set up

* ``bin/robot`` executes Robot Framework's ``pybot``-runner so that it
  will run the given test suite against the running ``robot-server``,
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

Once the test server has started, there should be a test Plone-site served at
http://localhost:55001/plone/ (by default). This allows you to play with the
sandbox while writing the tests.

.. note:: The default admin user for `plone.app.testing`_-based Plone-sandbox
   is ``admin`` and password is ``secret``.


Write your first test suite
---------------------------

Robot tests are written in test suites, which are plain text files, usually
ending with ``.robot`` (and older ones with ``.txt``).

The first test can be written anywhere in the filesystem.


For example, a ``test_hello.robot`` :

.. code-block:: robotframework

   *** Settings ***

    Force Tags  wip-not_in_docs

    Resource  plone/app/robotframework/selenium.robot
    Test Setup  Plone test setup
    Test Teardown  Plone test teardown

  *** Test Cases ***

    Plone is installed
      Go to  ${PLONE_URL}
      Page should contain  Powered by Plone


Robot is all about running test clauses called **keywords** (or, to be more
exact, keyword calls with parameters). Every test case may contain one or more
keywords, which are run sequentially -- usually until the first of them fails.
Keywords are separated from their arguments (and arguments from each other)
using at least two spaces.

Keywords are defined in **keyword libraries** and as **user keywords**. Keyword
libraries can be Python libraries or XML-RPC-services. User keywords are just
lists of test clauses reusing existing keywords or other user keywords. User
keywords are described in the test suite, or imported from **resource** files.

Here is a more complicated example with some user keywords in action:

.. code-block:: robotframework

   *** Settings ***

    Force Tags  wip-not_in_docs

    Resource  plone/app/robotframework/saucelabs.robot
    Resource  plone/app/robotframework/selenium.robot

    Library  Remote  ${PLONE_URL}/RobotRemote

    Test Setup  Plone test setup
    Test Teardown  Plone test teardown

    *** Variables ***

    ${ADMIN_ROLE}  Site Administrator

    *** Test Cases ***

    Site Administrator can access control panel
        Given I'm logged in as a '${ADMIN_ROLE}'
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


Please, stop for a while end read the example above again. Once you understand
how you can stack keyword calls with user keywords, you are ready to unleash
the power of Robot Framework all the way to building your own domain specific
test language.

.. note:: We use ``.robot`` as the Robot Framework test suite file extension
   to make it easier for developers to configure Robot Framework syntax
   highlighting for their editors (otherwise ``.txt`` would work also).


Run your first test suite
-------------------------

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

It's often convenient to run Robot tests with other Plone tests (e.g. on
Jenkins or Travis-CI). To achieve that, we integrate Robot tests to be run with
other tests so that all tests can be run with `zope.testrunner`_.

.. _zope.testrunner: http://pypi.python.org/pypi/zope.testrunner

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

`RobotSuite`_ is our package for wrapping Robot Framework tests into Python
unittest compatible test cases. It's good to know that this registration
pattern is the same as how doctest-suites are registered to support
*zope.testrunner*'s layers (see https://pypi.python.org/pypi/plone.testing for
layered doctest examples).


Running tests with zope.testrunner
----------------------------------

Once your robot test have been integrated with *zope.testrunner* using
``test_robot.py``-module (or any other module returning RobotTestSuite),
you can list your integrated robot test cases with command:

.. code-block:: bash

   $ bin/test --list-tests

And run robot tests cases with all other test cases with command:

.. code-block:: bash

   $ bin/test

You can filter robot test using ``-t``-argument for zope.testrunner*:

.. code-block:: bash

   $ bin/test -t robot

And it's also possible to filter test by Robot Framework tags:

.. code-block:: bash

   $ bin/test -t \#mytag

Or exclude matching tests from being run:

.. code-block:: bash

   $ bin/test -t \!robot


Running tests with a different browser
--------------------------------------

Our robot configuration uses Firefox to run robot tests per default.
To change this, you can pass an environment variable to zope.testrunner script.
Make sure, any necessary webdriver applications are installed along with your browser (Firefox until version 46 ships with one preinstalled).
Run your tests like so::

    ROBOT_BROWSER=BROWSER_CONFIG_NAME ./bin/test --all -m MODULE_TO_TEST

The browser name is a configuration variable from Selenium2Library.
The most important ones are::

- android
- chrome
- firefox
- internetexplorer
- iphone
- opera
- phantomjs
- safari

For more information see: http://robotframework.org/Selenium2Library/Selenium2Library.html#Open%20Browser

In case for Google Chrome, do the following:

* Install the ``ChromeDriver`` from https://sites.google.com/a/chromium.org/chromedriver/
  ChromeDriver needs to be accessible from your path.

* Start the tests like so (An example testing the ``test_tinymce.robot`` test from ``Products.CMFPlone``)::

    ROBOT_BROWSER=chrome ./bin/test --all -m Products.CMFPlone -t test_tinymce.robot


.. note::
    If you want to run the tests with a different Firefox version than already installed, you can do the following (this applies to Linux based Systems):

    1) Download the required version from https://ftp.mozilla.org/pub/firefox/releases/

    2) Unzip it in a folder

    3) Modify the ``PATH`` environment variable in a terminal to include the firefox binary before any other, like so::

        $ export PATH=/home/user/Desktop/firefox43:$PATH

    4) Run the tests in the same terminal session, where the modified PATH applies::

        $ ./bin/test --all -m Products.CMFPlone -t test_tinymce.robot


How to write more tests
-----------------------

The most difficult part in writing robot tests with Selenium-keywords is to
know the application you are testing: which link to click when and to which
field to input test data.

At first, you should have a brief idea about the available keywords:

* `Robot Framework built-in library documentation`__
* `Robot Framework Selenium2Library documentation`__

__ http://robotframework.org/robotframework/latest/libraries/BuiltIn.html
__ http://rtomac.github.com/robotframework-selenium2library/doc/Selenium2Library.html

Then, learn to use pause test execution to make it easier to figure out,
what to do next:

.. code-block:: robotframework

    *** Settings ***



    Resource  plone/app/robotframework/selenium.robot

    Library  Remote  ${PLONE_URL}/RobotRemote

    Test Setup  Plone test setup
    Test Teardown  Plone test teardown

    *** Test Cases ***

    Let me think what to do next
        Enable autologin as  Site Administrator
        Go to  ${PLONE_URL}

        Import library  Dialogs
        Pause execution

Robot Framework ships with a few selected standard libraries. One of them is
the *Dialogs*-library, which provides a very useful keyword: *Pause execution*.
By importing Dialogs-library (while developing the test) and adding the *Pause
execution* keyword, you can pause the test at any point to make it possible to
figure out what to do next.
(Dialogs depend on `TkInter-library <http://wiki.python.org/moin/TkInter>`_.)

.. note:: Be sure to remove *Import libary* and *Pause execution*
   keyword calls before committing your tests to avoid pausing your
   tests on CI.

.. note:: *plone.app.robotframework* ships with an optional collection
   of Plone-specific user keywords, which already include *Pause* keyword as a
   shortcut for *Pause execution* keywords. You can include and use the
   collection with:

   .. code-block:: robotframework

      *** Settings ***



      ...

      Resource  plone/app/robotframework/keywords.robot

      *** Test Cases ***

      Let me think what to do next
          ...
          Pause
