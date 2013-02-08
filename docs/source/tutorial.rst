Getting started with Robot Framework and plone.app.testing
==========================================================

.. warning::
     This documentation has not been updated for ``plone.act`` yet.

Selenium testing Plone doesn't need to be difficult.
Actually, with the recent hard work done for
`robotframework-selenium2library <https://github.com/rtomac/robotframework-selenium2library>`_
it's the easiest way to test your add-ons!
(`Thanks a lot to these folks! <https://github.com/rtomac/robotframework-selenium2library/graphs/contributors>`_)

I'll show you, how to create your first
`zope.testrunner <http://pypi.python.org/pypi/zope.testrunner>`_
compatible Robot Framework tests for your custom Plone add-on.
Also, everything you already know about
`plone.app.testing <http://pypi.python.org/pypi/plone.app.testing>`_,
zope.testrunner or Python unittest-library, should apply here.


Environment
-----------

Here's our dummy Plone add-on package with its testing buildout::

    bootstrap.py
    buildout.cfg
    CHANGES.txt
    README.txt
    setup.py
    src
    src/my
    src/my_package
    src/my_package/__init__.py
    src/my_package/tests
    src/my_package/tests/__init__.py
    src/my_package/tests/test_acceptance.py
    src/my_package/tests/test_accessibility.txt

We've got
`bootstrap.py <https://raw.github.com/plone/buildout.coredev/4.2/bootstrap.py>`_
from Plone `coredev-buildout <http://github.com/plone/buildout.coredev>`_,
empty text files for ``README`` and ``CHANGES``, and the following ``setup.py``
to define our (empty) add-on package::

    from setuptools import setup, find_packages

    version = "1.0.0"

    setup(
        name="my-package",
        version=version,
        description="An example Plone add-on",
        long_description=open("README.txt").read() + "\n" +
                         open("CHANGES.txt").read(),
        # Get more strings from
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
        classifiers=[
            "Programming Language :: Python",
        ],
        keywords="",
        author="",
        author_email="",
        url="",
        license="GPL",
        packages=find_packages("src", exclude=["ez_setup"]),
        package_dir={"": "src"},
        include_package_data=True,
        zip_safe=False,
        install_requires=[
            "setuptools",
        ],
        extras_require={"test": [
            "plone.app.testing",
            "robotsuite",
            "robotframework-selenium2library"],
        },
        entry_points="""
        # -*- Entry points: -*-
        [z3c.autoinclude.plugin]
        target = plone
        """
        )

Note, how we've defined ``test``-extras for our package to require
`robotsuite <http://pypi.python.org/pypi/robotsuite>`_ and
`robotframework-selenium2library <http://pypi.python.org/pypi/robotframework-selenium2library>`_
packages in addition to the usual ``plone.app.testing``.

And here's our ``buildout.cfg`` to set up the test runner::

    [buildout]
    extends = http://dist.plone.org/release/4.2-latest/versions.cfg
    parts = test
    develop = .

    [test]
    recipe = zc.recipe.testrunner
    eggs = my-package [test]


Test suite
----------

Let's write our first test suite in Robot Framework syntax into
``src/my_package/tests/test_accessibility.txt``::

    *** Settings ***

    Library  Selenium2Library  timeout=10  implicit_wait=0.5

    Suite Setup  Start browser
    Suite Teardown  Close All Browsers

    *** Test Cases ***

    Plone Accessibility
        Goto homepage
        Click link  Accessibility
        Page should contain  Accessibility Statement

    *** Keywords ***

    Start browser
        Open browser  http://localhost:55001/plone/

    Goto homepage
        Go to  http://localhost:55001/plone/
        Page should contain  Plone site

Note, how we import and configure **Selenium2Library**, and how we expect Plone
to be found at ``http://localhost:55001/plone/``. That's how
``plone.app.testing`` serves it.


Robotsuite
----------

The last step is to glue our Robot Framework test suite and
``plone.app.testing`` together. That's done with ``robotsuite``-package by
defining new a **RobotTestSuite** with the default **PLONE_ZSERVER**-layer from
``plone.app.testing`` in ``src/my_package/tests/test_acceptance.py``::

    import unittest

    from plone.testing import layered
    from plone.app.testing import PLONE_ZSERVER

    import robotsuite


    def test_suite():
        suite = unittest.TestSuite()
        suite.addTests([
            layered(robotsuite.RobotTestSuite("test_accessibility.txt"),
                    layer=PLONE_ZSERVER),
        ])
        return suite

If you have ever defined a Python doctest test suite to be used with
``plone.app.testing``, the above should look very familiar.


Running
-------

With everything above in place, just run:

1. bootstrap (with a Plone-compatible Python or virtualenv)::

        $ python bootstrap.py

2. buildout::

        $ bin/buildout

3. and test::

        $ bin/test

and you should see something like::

    $ python bootstrap.py
    Downloading http://pypi.python.org/packages/source/d/distribute/distribute-0.6.28.tar.gz
    Extracting in /var/folders/b1/mld_r9wj1jbfwf2jcfl_d61sc6kdnb/T/tmp902seC
    Now working in /var/folders/b1/mld_r9wj1jbfwf2jcfl_d61sc6kdnb/T/tmp902seC/distribute-0.6.28
    Building a Distribute egg in /var/folders/b1/mld_r9wj1jbfwf2jcfl_d61sc6kdnb/T/tmp69NImk
    /var/folders/b1/mld_r9wj1jbfwf2jcfl_d61sc6kdnb/T/tmp69NImk/distribute-0.6.28-py2.7.egg
    Creating directory '/.../bin'.
    Creating directory '/.../parts'.
    Creating directory '/.../develop-eggs'.
    Generated script '/.../bin/buildout'.

    $ bin/buildout
    Develop: '/.../.'
    Installing test.
    ...
    Generated script '/.../bin/test'.

    $ bin/test
    Running plone.app.testing.layers.Plone:ZServer tests:
      Set up plone.testing.zca.LayerCleanup in 0.000 seconds.
      Set up plone.testing.z2.Startup in 0.398 seconds.
      Set up plone.app.testing.layers.PloneFixture in 9.921 seconds.
      Set up plone.testing.z2.ZServer in 0.506 seconds.
      Set up plone.app.testing.layers.Plone:ZServer in 0.000 seconds.
      Ran 1 tests with 0 failures and 0 errors in 2.969 seconds.
    Tearing down left over layers:
      Tear down plone.app.testing.layers.Plone:ZServer in 0.000 seconds.
      Tear down plone.app.testing.layers.PloneFixture in 0.088 seconds.
      Tear down plone.testing.z2.ZServer in 5.151 seconds.
      Tear down plone.testing.z2.Startup in 0.009 seconds.
      Tear down plone.testing.zca.LayerCleanup in 0.005 seconds.

You should also find Robot Framework logs and reports being generated into your
buildout directory under ``parts/test``.


Custom layer
------------

Obviously, we'd like to run our test against a Plone with our own
add-on installed. That requires a custom test layer, as described at
`plone.app.testing <http://pypi.python.org/pypi/plone.app.testing>`_.

Let's start by adding a few more files::

    src/my_package/configure.zcml
    src/my_package/hello_world.pt
    src/my_package/testing.py
    src/my_package/tests/test_hello_world.txt

At first we define our custom view to be tested in
``src/my_package/configure.zcml``::

    <configure xmlns="http://namespaces.zope.org/zope"
               xmlns:browser="http://namespaces.zope.org/browser">

        <browser:page
            name="hello-world"
            for="Products.CMFCore.interfaces.ISiteRoot"
            template="hello_world.pt"
            permission="zope2.View"
            />

    </configure>

and in ``src/my_package/hello_world.pt``::

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

Then we define our custom test layer in ``src/my_package/testing.py``::

    from plone.app.testing import (
        PloneSandboxLayer,
        FunctionalTesting,
        PLONE_FIXTURE,
    )

    from plone.testing.z2 import ZSERVER_FIXTURE


    class MyPackageLayer(PloneSandboxLayer):
        defaultBases = (PLONE_FIXTURE,)

        def setUpZope(self, app, configurationContext):
            import my_package
            self.loadZCML(package=my_package)


    MY_PACKAGE_FIXTURE = MyPackageLayer()

    MY_PACKAGE_ACCEPTANCE_TESTING = FunctionalTesting(
        bases=(MY_PACKAGE_FIXTURE, ZSERVER_FIXTURE),
        name="MyPackage:Acceptance")

Note, how we build on top of **PloneSandboxLayer** and how we create our final
acceptance test layer by combining our custom **MY_PACKAGE_FIXTURE** and
**ZSERVER_FIXTURE**. The latter would make our Plone sandbox served at
``http://localhost:55001/``. Finally, **FunctionalTesting** gives us a clean
isolated Plone site to be played with for each test case.

Finally, we write a new Robot Framework test suite into
``src/my_package/tests/test_hello_world.txt``::

    *** Settings ***

    Library  Selenium2Library  timeout=10  implicit_wait=0.5

    Suite Setup  Start browser
    Suite Teardown  Close All Browsers

    *** Test Cases ***

    Hello World
        Go to  http://localhost:55001/plone/hello-world
        Page should contain  Hello World!

    *** Keywords ***

    Start browser
        Open browser  http://localhost:55001/plone/

We can now include our new test suite in
``src/my_package/tests/test_acceptance.py``::

    import unittest

    from plone.testing import layered
    from plone.app.testing import PLONE_ZSERVER

    from my_package.testing import MY_PACKAGE_ACCEPTANCE_TESTING

    import robotsuite


    def test_suite():
        suite = unittest.TestSuite()
        suite.addTests([
            layered(robotsuite.RobotTestSuite("test_accessibility.txt"),
                    layer=PLONE_ZSERVER),
            layered(robotsuite.RobotTestSuite("test_hello_world.txt"),
                    layer=MY_PACKAGE_ACCEPTANCE_TESTING),
        ])
        return suite

and re-run our tests::

    $ bin/test --list-tests
    Listing my_package.testing.MyPackage:Acceptance tests:
      Hello_World (test_hello_world.txt)
    Listing plone.app.testing.layers.Plone:ZServer tests:
      Plone_Accessibility (test_accessibility.txt)

    $ bin/test
    Running my_package.testing.MyPackage:Acceptance tests:
      Set up plone.testing.zca.LayerCleanup in 0.000 seconds.
      Set up plone.testing.z2.Startup in 0.219 seconds.
      Set up plone.app.testing.layers.PloneFixture in 7.204 seconds.
      Set up my_package.testing.MyPackageLayer in 0.028 seconds.
      Set up plone.testing.z2.ZServer in 0.503 seconds.
      Set up my_package.testing.MyPackage:Acceptance in 0.000 seconds.
      Ran 1 tests with 0 failures and 0 errors in 2.493 seconds.
    Running plone.app.testing.layers.Plone:ZServer tests:
      Tear down my_package.testing.MyPackage:Acceptance in 0.000 seconds.
      Tear down my_package.testing.MyPackageLayer in 0.002 seconds.
      Set up plone.app.testing.layers.Plone:ZServer in 0.000 seconds.
      Ran 1 tests with 0 failures and 0 errors in 2.213 seconds.
    Tearing down left over layers:
      Tear down plone.app.testing.layers.Plone:ZServer in 0.000 seconds.
      Tear down plone.app.testing.layers.PloneFixture in 0.091 seconds.
      Tear down plone.testing.z2.ZServer in 5.155 seconds.
      Tear down plone.testing.z2.Startup in 0.009 seconds.
      Tear down plone.testing.zca.LayerCleanup in 0.005 seconds.
    Total: 2 tests, 0 failures, 0 errors in 18.305 seconds.


Logging in
----------

``plone.app.testing`` defines a test user for our test site, but how could our
Robot Framework test know her login credentials? Well, we have to make our test
to ask for the credentials by defining custom Robot Framework test keywords
in Python.

Let's add a couple of more files, as in::

    src/my_package/testing_keywords.py
    src/my_package/tests/test_login.txt

At first, we type our custom Robot Framework keyword library with test keywords
for retrieving the test users credentials into
``src/my_package/testing_keywords.py``::

    class Keywords(object):
        """Robot Framework keyword library"""

        def get_test_user_name(self):
            import plone.app.testing
            return plone.app.testing.interfaces.TEST_USER_NAME

        def get_test_user_password(self):
            import plone.app.testing
            return plone.app.testing.interfaces.TEST_USER_PASSWORD

Then, we can write our new login test into
``src/my_package/tests/test_login.txt``::

    *** Settings ***

    Library  Selenium2Library  timeout=10  implicit_wait=0.5
    Library  my_package.testing_keywords.Keywords

    Suite Setup  Start browser
    Suite Teardown  Close All Browsers

    *** Test Cases ***

    Log in
        ${TEST_USER_NAME} =  Get test user name
        ${TEST_USER_PASSWORD} =  Get test user password
        Go to  http://localhost:55001/plone/login_form
        Page should contain element  __ac_name
        Input text  __ac_name  ${TEST_USER_NAME}
        Input text  __ac_password  ${TEST_USER_PASSWORD}
        Click Button  Log in
        Page should contain element  css=#user-name

    *** Keywords ***

    Start browser
        Open browser  http://localhost:55001/plone/

Note, how we can import our custom keyword library right after
**Selenium2Libary**. Also, see how we use our custom keywords to retrieve test
user's login credentials into Robot Framework test variables and how we use
them later in the test.

We can now include our new test suite in
``src/my_package/tests/test_acceptance.py``::

    import unittest

    from plone.testing import layered
    from plone.app.testing import PLONE_ZSERVER

    from my_package.testing import MY_PACKAGE_ACCEPTANCE_TESTING

    import robotsuite


    def test_suite():
        suite = unittest.TestSuite()
        suite.addTests([
            layered(robotsuite.RobotTestSuite("test_accessibility.txt"),
                    layer=PLONE_ZSERVER),
            layered(robotsuite.RobotTestSuite("test_hello_world.txt"),
                    layer=MY_PACKAGE_ACCEPTANCE_TESTING),
            layered(robotsuite.RobotTestSuite("test_login.txt"),
                    layer=PLONE_ZSERVER),
        ])
        return suite

and re-run our tests::

    $ bin/test --list-tests
    Listing my_package.testing.MyPackage:Acceptance tests:
      Hello_World (test_hello_world.txt)
    Listing plone.app.testing.layers.Plone:ZServer tests:
      Plone_Accessibility (test_accessibility.txt)
      Log_in (test_login.txt)

    $ bin/test
    Running my_package.testing.MyPackage:Acceptance tests:
      Set up plone.testing.zca.LayerCleanup in 0.000 seconds.
      Set up plone.testing.z2.Startup in 0.217 seconds.
      Set up plone.app.testing.layers.PloneFixture in 7.132 seconds.
      Set up my_package.testing.MyPackageLayer in 0.026 seconds.
      Set up plone.testing.z2.ZServer in 0.503 seconds.
      Set up my_package.testing.MyPackage:Acceptance in 0.000 seconds.
      Ran 1 tests with 0 failures and 0 errors in 2.473 seconds.
    Running plone.app.testing.layers.Plone:ZServer tests:
      Tear down my_package.testing.MyPackage:Acceptance in 0.000 seconds.
      Tear down my_package.testing.MyPackageLayer in 0.002 seconds.
      Set up plone.app.testing.layers.Plone:ZServer in 0.000 seconds.
      Ran 2 tests with 0 failures and 0 errors in 7.766 seconds.
    Tearing down left over layers:
      Tear down plone.app.testing.layers.Plone:ZServer in 0.000 seconds.
      Tear down plone.app.testing.layers.PloneFixture in 0.088 seconds.
      Tear down plone.testing.z2.ZServer in 5.156 seconds.
      Tear down plone.testing.z2.Startup in 0.009 seconds.
      Tear down plone.testing.zca.LayerCleanup in 0.005 seconds.
    Total: 3 tests, 0 failures, 0 errors in 23.765 seconds.


Debugging
---------

There's one catch in debugging your code while running Robot Framework tests.
It eats your standard input and output, which prevents you to just ``import
pdb; pdb.set_trace()``. Instead, you have to add a few more lines to reclaim
your I/O at first, and only then let your debugger in::

    import sys
    for attr in ('stdin', 'stdout', 'stderr'):
        setattr(sys, attr, getattr(sys, '__%s__' % attr))
    import pdb; pdb.set_trace()

Note, you need to put this into the Plone Python code. Robot Framework does not 
understand Python.

To better follow the Webdriver carrie out your test you can slow it down::

    Set Selenium Speed  0.5 seconds

You can pause Webdriver and inspect your step::
    
    Set Selenium Timeout  600 seconds
    Wait For Condition  true


Resources
---------

* `Selenium2Library keywords <http://rtomac.github.com/robotframework-selenium2library/doc/Selenium2Library.html>`_
* `Robot Framework built-in keywords <http://robotframework.googlecode.com/hg/doc/libraries/BuiltIn.html?r=2.7.3>`_
