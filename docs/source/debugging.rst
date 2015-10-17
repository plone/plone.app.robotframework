Debugging Robot Framework tests
===============================

It's not always so easy to get the used Selenium keywords right. There are
a few ways to pause the test runner in middle of a test to ease figuring out
what to do next:

1. Set the variable ``SELENIUM_RUN_ON_FAILURE`` to use the Debug-keyword
   provided in ``plone/app/robotframework/keywords.robot`` resource file,
   e.g. with:

   .. code-block:: bash

      $ ROBOT_SELENIUM_RUN_ON_FAILURE=Debug bin/test -t robot

   Or when testing against robot-server, just run your test suite with provided
   script:

   .. code-block:: bash

      $ bin/robot-debug src/path/to/my/test.robot

   This will stop the test automatically at the first failing step with the
   first working approach listed also below.

2. Use interactive `robotframework-debuglibrary`_ with *Debug*-keyword'
   (requires that the used python is compiled with readline-support):

   .. code-block:: robotframework


      *** Settings ***

      Force Tags  wip-not_in_docs

      *** Test Cases ***

      Start interactive debugger with Debug-keyword from DebugLibrary
          Import library  DebugLibrary
          Debug

3. Pause Selenium (WebDriver) completely to inspect your step with
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

4. Let Selenium (WebDriver) sleep for long time:

   .. code-block:: robotframework

      *** Test Cases ***

      Pause test with non-interactive (and auto-continuing) sleep
         Sleep  10 min

5. Slow down Selenium (WebDriver) to make the tests easier to follow:

   .. code-block:: robotframework

      *** Settings ***

      Suite setup  Set Selenium speed  0.5s

6. Use provided Python keyword to drop Zope server (or Robot Framework
   test runner) into debugger:

   .. code-block:: robotframework

      *** Test Cases ***

      Pause test with Python debugger
           Import library  plone.app.robotframework.Debugging
           Stop

7. Write a custom python keyword into your custom Python keyword library
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
