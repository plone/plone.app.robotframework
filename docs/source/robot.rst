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


Test suite
----------

Robot tests are written in test suites, which are plain text files, usually
ending with ``.robot`` (or just ``.txt``).

.. note:: Advanced robot users may learn from the `Robot Framework User Guide`_
   how to make hierarchical test suites.

.. _Robot Framework User Guide: http://code.google.com/p/robotframework/wiki/UserGuideRobot

Let's look into this example test suite in detail:

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

There's a little bit more of BDD-style tests in `Robot Framework User Guide`_.
