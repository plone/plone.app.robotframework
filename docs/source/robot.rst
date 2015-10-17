Robot terminology
=================

Robot Framework is a generic and independent test automation framework.
It has its own expandable test syntax, test runner and test reporting tools.
Yet, because of its extensibility it's very pleasant to work with.

Robot is all about running test clauses called **keywords** (or, to be more
exact, keyword calls with parameters). Every test case may contain one or more
keywords, which are run sequentially -- usually until the first of them fails.
Keyword arguments use two spaces as a separator. Keywords are separated from
their arguments (and arguments from each other) using at least two spaces.

Keywords are defined in **keyword libraries** and as **user keywords**. Keyword
libraries can be Python libraries or XML-RPC-services. User keywords are just
lists of test clauses reusing existing keywords or other user keywords. User
keywords are described in the test suite, or imported from **resource** files.


Test suites
-----------

Robot tests cases are written in test suites, which are plain text files,
usually ending with ``.robot`` (or just ``.txt``).

.. note:: Advanced robot users may learn from the `Robot Framework User Guide`_
   how to make hierarchical test suites.

.. _Robot Framework User Guide: http://code.google.com/p/robotframework/wiki/UserGuideRobot

Let's look into an example test suite in detail:

.. robot-source::
   :source: plone.app.robotframework:tests/docs/test_keywords.robot

Each test suite may contain one to four different parts:

**Settings**
    Is used to import available keyword libraries or resources
    (resources are plain text files like test suites, but without test cases)
    and define possible setup and teardown keywords.

**Variables**
    Is used to define available robot variables with their default values,
    or override variables defined in imported resources.

**Test Cases**
    Is used to define runnable tests cases, which are made of test clauses
    calling test keywords.

**Keywords**
    Is used to define new user keywords, which may re-use existing keywords
    from imported libraries or resource files.


Keywords libraries
------------------

By default, only keywords from `built-in`_-library are available to be used in
tests. Other keywords must be included by importing a keyword library in
*Settings* part of test suite:

.. code-block:: robotframework

   *** Settings ***

   Force Tags  wip-not_in_docs

   Library  String
   Library  Selenium2Library

.. _built-in: http://robotframework.googlecode.com/hg/doc/libraries/BuiltIn.html

View `the complete list of available keyword libraries shipped with
Robot Framework or available as separate package`__.

__ http://code.google.com/p/robotframework/wiki/TestLibraries

.. note:: Libraries may also be included in resource files, and then it's
   enough to import such resource file.

There's also a built-in-keyword ``Import Library`` for importing library
in a middle of test case or keyword:

.. code-block:: robotframework

   *** Test Cases ***

   Test Import library keyword
       Import library  String


Remote keyword libraries
------------------------

One of the available keyword libraries (shipped with Robot Framework) is
special: `Remote`_-library. Remote-library makes it possible to provide test
keywords from an XML-RPC-service, for example, from a public Zope2-object.

.. _remote: http://robotframework.googlecode.com/hg/doc/userguide/RobotFrameworkUserGuide.html#remote-library-interface

*plone.app.robotframework*-provides convention and helpers to enable
customizable set of remote keywords in Python as a public portal-tool object
called ``RobotRemote``. These keywords can be imported with:

.. code-block:: robotframework

   *** Settings ***

   Resource  plone/app/robotframework/selenium.robot

   Library  Remote  ${PLONE_URL}/RobotRemote

Remote-library approach provides the following benefits when testing Plone:

* All test setup keywords can be implemented in Python, which makes their
  execution almost instant when compared to executing similar steps in
  Selenium (to make your Selenium tests as fast as possible only the really
  meaningful steps should be executed through Selenium).

* Each keyword call is executed as a normal transaction in Plone, which
  makes all code behave normally as in real use.

* When e.g.
  :download:`content creation (remote) keywords <libdoc/remote_autologin.html>`
  are called with
  :download:`autologin <libdoc/remote_content.html>`
  enabled, all actions are performed as the autologin user so author
  metadata etc is created correctly.


Resource files
--------------

Resource files provide a re-usable way to abstract your test suites. To put
it simply, resources files are just like all the other ``.robot``-files, but
they should not contain ``*** Test Cases ***`` certain ``*** Settings ***``
commands (*Suite Setup*, *Suite Teardown*, *Test Setup* or *Test Teardown*).

Resource files are the perfect way to import common libraries (with *Library*
command in ```*** Settings ***``), define global ``*** Variables ***`` and
define re-usable common ```*** Keywords ***```. Resource files are included
in a test suite with *Resource*-command in ```*** Settings ***``:

.. code-block:: robotframework

   *** Settings ***

   Resource  plone/app/robotframework/keywords.robot
   Resource  plone/app/robotframework/selenium.robot
   Resource  plone/app/robotframework/saucelabs.robot


BDD-style tests
---------------

Robot support Gherkin-style tests by removing exact words ``given``,
``when``, ``then`` and ``and`` from the beginning of keyword to find
a matching keyword.

For example, a clause ``Given I'm logged in as an admin``:

.. code-block:: robotframework

   *** Test Cases ***

   Test something as logged in admin
       Given I'm logged in as an admin

will match to a keyword ``I'm logged in as an admin``:

.. code-block:: robotframework

   *** Keywords ***

   I'm logged in as an admin
       Enable autologin as  Manager

There's a little bit more of BDD-style tests available in `Robot Framework User
Guide`_.
