Learn more robot
================

Robot Framework is a generic and independent test automation framework with its
own expandable test syntax, test runner and test reporting tools. Yet, because
of its extensibility it's very pleasant to work with.

Robot is all about running test clauses called **keywords**. Every test may
contain one more keywords, which are run in serial -- usually until first of
them fails.

Keywords are defined in **keywords libraries** and as **user keywords**.
Keyword libraries may be, for example, Python libraries or XML-RPC-services.
User keywords are just composite lists of existing keywords -- also user
keywords.

Because user keywords can also be composite of other user keywords,
they make it possible to write tests in domain-specific language.


Test suite
----------

Robot tests are written in test suites, which are simply plain text files,
usually ending with ``.txt``.

.. note::

   Advanced robot users may learn from the
   `Robot Framework User Guide <http://code.google.com/p/robotframework/wiki/UserGuideRobot>`_
   how to make hierarchical test suites.

Here's an example test suite::

    *** Settings ***

    Library  Selenium2Library  timeout=10  implicit_wait=0.5
    Resources  keywords.txt

    Suite Setup  Start browser
    Suite Teardown  Close All Browsers

    *** Variables ***

    ${BROWSER} =  firefox

    *** Test Cases ***

    Hello World
        [Tags]  hello
        Go to  http://localhost:55001/plone/hello-world
        Page should contain  Hello World!

    *** Keywords ***

    Start browser
        Open browser  http://localhost:55001/plone/  browser=${BROWSER}

Each test suite may contain one to three different parts::

**Settings**
    Import available keyword libraries or resources (resources are
    plain text files like test suites, but without test cases) and
    define possible setup and teardown keywords.

**Variables**
    Define available robot variables with their default values.

**Test Cases**
    Define runnable tests.

**Keywords**
    Define new user keywords.


BDD-style tests
---------------

Robot support Gherkin-style tests by removing exact words ``given``,
``when``, ``then`` and ``and`` from the beginning of keyword to find
a matching keyword.

For example, a clause::

    Given I'm logged in as an admin

will match to a keyword::

    I'm logged in as an admin

There's a little bit more of BDD-style tests in
`Robot Framework User Guide
<http://robotframework.googlecode.com/hg/doc/userguide/RobotFrameworkUserGuide.html?r=2.7.6#behavior-driven-stylep>`_.
