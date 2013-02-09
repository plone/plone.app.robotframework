How to write a robot test for a Plone add-on
============================================

This is a minimal tutorial to get started with writing functional Selenium
tests for Plone with Robot Framework.


Setup Templer
-------------

At first, we should have an add-on to test with. For creating a new add-on, we
use `Templer <http://templer-manual.readthedocs.org/en/latest/>`_.

1. Create a new
`Python virtualen <http://www.virtualenv.org/>`_
for Templer installation::

    $ virtualenv -p /usr/bin/python2.7 templerenv
    Running virtualenv with interpreter /usr/bin/python2.7
    New python executable in templerenv/bin/python
    Installing setuptools............done.
    Installing pip...............done.

2. Activate the new virtualenv::

    $ source templerenv/bin/activate

3. Install Templer on it::

    $ pip install templer.core
    Downloading/unpacking templer.core
    ...
    Cleaning up...

4. And install Plone-templates for Templer on it::

    $ pip install templer.plone
    Downloading/unpacking templer.plone
    ...
    Cleaning up...

Leave the virtualenv active for the next step.


Create a new product
--------------------

Once we have Templer installed, we can create a Plone add-on product by
entering command ``templer plone_basic`` and answering for the upcoming
questions::

    $templer plone_basic

    plone_basic: A package for Plone add-ons

    This template creates a package for a basic Plone add-on project with
    a single namespace (like Products.PloneFormGen).

    To create a Plone project with a name like 'collective.geo.bundle'
    (2 dots, a 'nested namespace'), use the 'plone_nested' template.

    If you are trying to create a Plone *site* then the best place to
    start is with one of the Plone installers.  If you want to build
    your own Plone buildout, use one of the plone'N'_buildout templates


    This template expects a project name with 1 dot in it (a 'basic
    namespace', like 'foo.bar').

    Enter project name (or q to quit): my.product

    If at any point, you need additional help for a question, you can enter
    '?' and press RETURN.

    Expert Mode? (What question mode would you like? (easy/expert/all)?) ['easy']:
    Version (Version number for project) ['1.0']:
    Description (One-line description of the project) ['']:
    Register Profile (Should this package register a GS Profile) [False]:
    Creating directory ./my.product
    Replace 1019 bytes with 1364 bytes (2/43 lines changed; 8 lines added)
    Replace 42 bytes with 119 bytes (1/1 lines changed; 4 lines added)

Once we have answered for all the questions. Our add-on template is ready.

If we installed Templer into its own virtualenv, we can deactivate it now
with::

    $ deactivate


Update requirements
-------------------

``my.product/setup.py``::

      extras_require={'test': ['plone.app.testing',
                               'robotsuite',
                               'robotframework-selenium2library',
                               'decorator',
                               'selenium']},


Bootstrap and run buildout
--------------------------

::

    $ python bootstrap.py --distribute
    $ bin/buildout



Define functional test fixture
------------------------------


``my.product/src/my/product/testing.py``::

    from plone.app.testing import FunctionalTesting


    MY_PRODUCT_FUNCTIONAL_TESTING = FunctionalTesting(
        bases=(MY_PRODUCT_FIXTURE, z2.ZSERVER_FIXTURE),
        name="MyproductLayer:Functional"
    )


Create robot test suite
-----------------------

``my.product/src/my/product/tests/robot_hello.txt``::

    *** Settings ***

    Library  Selenium2Library  timeout=10  implicit_wait=0.5

    Suite Setup  Start browser
    Suite Teardown  Close All Browsers

    *** Test Cases ***

    Hello World
        [Tags]  hello
        Go to  http://localhost:55001/plone/hello-world
        Page should contain  Hello World!

    *** Keywords ***

    Start browser
        Open browser  http://localhost:55001/plone/


Register the suite for zope.testrunner
--------------------------------------

``my.product/src/my/product/tests/test_robot.py``::

    from my.product.testing import MY_PRODUCT_FUNCTIONAL_TESTING
    from plone.testing import layered
    import robotsuite
    import unittest


    def test_suite():
        suite = unittest.TestSuite()
        suite.addTests([
            layered(robotsuite.RobotTestSuite("robot_hello_world.txt"),
                    layer=MY_PRODUCT_FUNCTIONAL_TESTING)
        ])
        return suite


List and filter tests
---------------------

::

    $ bin/test --list-tests
    Listing my.product.testing.MyproductLayer:Functional tests:
      Hello_World (robot_hello_world.txt) #hello
    Listing my.product.testing.MyproductLayer:Integration tests:
      test_success (my.product.tests.test_example.TestExample)

::

    $ bin/test -t robot_ --list-tests
    Listing my.product.testing.MyproductLayer:Functional tests:
      Hello_World (robot_hello_world.txt) #hello

::

    $ bin/test -t \!robot_ --list-tests
    Listing my.product.testing.MyproductLayer:Integration tests:
      test_success (my.product.tests.test_example.TestExample)

::

    $ bin/test -t \#hello --list-tests
    Listing my.product.testing.MyproductLayer:Functional tests:
      Hello_World (robot_hello_world.txt) #hello


Run (failing) test
------------------

::

    $ bin/test -t robot_

    Running my.product.testing.MyproductLayer:Functional tests:
      Set up plone.testing.zca.LayerCleanup in 0.000 seconds.
      Set up plone.testing.z2.Startup in 0.217 seconds.
      Set up plone.app.testing.layers.PloneFixture in 7.643 seconds.
      Set up my.product.testing.MyproductLayer in 0.026 seconds.
      Set up plone.testing.z2.ZServer in 0.503 seconds.
      Set up my.product.testing.MyproductLayer:Functional in 0.000 seconds.
      Running:
        1/1 (100.0%)
    ==============================================================================
    Robot Hello World
    ==============================================================================
    Hello World                                                           | FAIL |
    Page should have contained text 'Hello World!' but did not
    ------------------------------------------------------------------------------
    Robot Hello World                                                     | FAIL |
    1 critical test, 0 passed, 1 failed
    1 test total, 0 passed, 1 failed
    ==============================================================================
    Output:  /.../my.product/parts/test/robot_hello_world/Hello World/output.xml
    Log:     /.../my.product/parts/test/robot_hello_world/Hello World/log.html
    Report:  /.../my.product/parts/test/robot_hello_world/Hello World/report.html



    Failure in test Hello World (robot_hello_world.txt) #hello
    Traceback (most recent call last):
      File "/.../unittest2-0.5.1-py2.7.egg/unittest2/case.py", line 340, in run
        testMethod()
      File "/.../eggs/robotsuite-1.0.1-py2.7.egg/robotsuite/__init__.py", line 312, in runTest
        assert last_status == 'PASS', last_message
    AssertionError: Page should have contained text 'Hello World!' but did not


      Ran 1 tests with 1 failures and 0 errors in 3.632 seconds.
    Tearing down left over layers:
      Tear down my.product.testing.MyproductLayer:Functional in 0.000 seconds.
      Tear down plone.testing.z2.ZServer in 5.282 seconds.
      Tear down my.product.testing.MyproductLayer in 0.003 seconds.
      Tear down plone.app.testing.layers.PloneFixture in 0.084 seconds.
      Tear down plone.testing.z2.Startup in 0.006 seconds.
      Tear down plone.testing.zca.LayerCleanup in 0.004 seconds.


Create an example view
----------------------


``my.product/src/my/product/configure.zcml``::

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:five="http://namespaces.zope.org/five"
        xmlns:browser="http://namespaces.zope.org/browser"
        xmlns:i18n="http://namespaces.zope.org/i18n"
        xmlns:genericsetup="http://namespaces.zope.org/genericsetup"
        i18n_domain="my.product">

      <five:registerPackage package="." initialize=".initialize" />

      <browser:page
          name="hello-world"
          for="Products.CMFCore.interfaces.ISiteRoot"
          template="hello_world.pt"
          permission="zope2.View"
          />

      <!-- -*- extra stuff goes here -*- -->

    </configure>


``my.product/src/my/product/hello_world.pt``::

    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
          xmlns:tal="http://xml.zope.org/namespaces/tal"
          xmlns:metal="http://xml.zope.org/namespaces/metal"
          xmlns:i18n="http://xml.zope.org/namespaces/i18n"
          lang="en"
          metal:use-macro="context/main_template/macros/master"
          i18n:domain="plone">
    <body>

    <metal:content-core fill-slot="content-core">
        <metal:content-core define-macro="content-core">
          <p>Hello World!</p>
        </metal:content-core>
    </metal:content-core>

    </body>
    </html>


Run (passing) test
------------------

::

    $ bin/test -t robot_
    Running my.product.testing.MyproductLayer:Functional tests:
      Set up plone.testing.zca.LayerCleanup in 0.000 seconds.
      Set up plone.testing.z2.Startup in 0.220 seconds.
      Set up plone.app.testing.layers.PloneFixture in 7.810 seconds.
      Set up my.product.testing.MyproductLayer in 0.027 seconds.
      Set up plone.testing.z2.ZServer in 0.503 seconds.
      Set up my.product.testing.MyproductLayer:Functional in 0.000 seconds.
      Running:

      Ran 1 tests with 0 failures and 0 errors in 2.604 seconds.
    Tearing down left over layers:
      Tear down my.product.testing.MyproductLayer:Functional in 0.000 seconds.
      Tear down plone.testing.z2.ZServer in 5.253 seconds.
      Tear down my.product.testing.MyproductLayer in 0.004 seconds.
      Tear down plone.app.testing.layers.PloneFixture in 0.085 seconds.
      Tear down plone.testing.z2.Startup in 0.006 seconds.
      Tear down plone.testing.zca.LayerCleanup in 0.004 seconds.


Test reports
------------

Robot Framework generates high quality test reports with screenshots of
failing tests:

``my.product/parts/tests/robot_report.html``
    Overview of the test results.

``my.product/parts/tests/robot_log.html``:
    Detailed log for every test with screenshots of failing tests.
