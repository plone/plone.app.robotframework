Debugging Robot Framework tests
===============================

It's not always so easy to get the used Selenium keywords right. There are
a few ways to pause the test runner in middle of a test to ease figuring out
what to do next:

1. Use interactive `robotframework-debuglibrary`_ with *Debug*-keyword'
   (requires that **plone.app.robotframework** is required with **[debug]**
   extras and the used python is compiled with readline-support):

      *** Settings ***

      Resource  plone/app/robotframework/keywords.robot

      *** Test Cases ***

      Start interactive debugger with included Debug-keyword
          Debug

2. Pause Selenium (WebDriver) completely to inspect your step with
   *Pause execution* keywords from *Dialogs*-library shipped with
   Robot Framework:

   .. code-block:: robotframework

      *** Test Cases ***

      Pause tests with interactive pause execution -keyword
         Import library  Dialogs
         Pause execution

   The above is also provided as *Pause*-keyword in ``keywords.robot``
   resource file:

   .. code-block:: robotframework

      *** Settings ***

      Resource  plone/app/robotframework/keywords.robot

      *** Test Cases ***

      Pause tests with included Pause-keyword
         Pause

3. Let Selenium (WebDriver) sleep for long time:

   .. code-block:: robotframework

      *** Test Cases ***

      Pause test with non-interactive (and auto-continuing) sleep
         Sleep  10 min

4. Slow down Selenium (WebDriver) to make the tests easier to follow:

   .. code-block:: robotframework

      *** Settings ***

      Suite setup  Set Selenium speed  0.5s

5. Use provided Python keyword to drop Zope server (or Robot Framework
   test runner) into debugger:

   .. code-block:: robotframework

      *** Test Cases ***

      Pause test with Python debugger
           Import library  plone.app.robotframework.Debugging
           Stop

6. Write a custom python keyword into your custom Python keyword library
   to drop Zope server (or Robot Framework test runner) into debugger.

   But there's one catch in debugging your code while running Robot Framework
   tests: Robot may eat your standard input and output, which prevents you to
   just ``import pdb; pdb.set_trace()``.

   Instead, you have to add a few more lines to reclaim your I/O at first, and
   only then let your debugger in:

   .. code-block:: python

      import sys
      import pdb
      for attr in ('stdin', 'stdout', 'stderr'):
          setattr(sys, attr, getattr(sys, '__%s__' % attr))
      pdb.set_trace()

.. _robotframework-debuglibrary: https://pypi.python.org/pypi/robotframework-debuglibrary
