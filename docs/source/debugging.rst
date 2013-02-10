Debugging robot tests
=====================

1. Slow done Selenium (WebDriver) to make the tests easier to follow::

    Set Selenium Speed  0.5 seconds


2. Pause Selenium (WebDriver) completely to inspect your step::

    Set Selenium Timeout  600 seconds
    Wait For Condition  true

3. Write a python keyword into your Python keyword library
   to drop the Zope server into debugger.

   There's one catch in debugging your code while running Robot Framework
   tests. Robot eats your standard input and output, which prevents you to just
   ``import pdb; pdb.set_trace()``.

   Instead, you have to add a few more lines to reclaim your I/O at first, and
   only then let your debugger in::

      import sys
      import pdb
      for attr in ('stdin', 'stdout', 'stderr'):
          setattr(sys, attr, getattr(sys, '__%s__' % attr))
      pdb.set_trace()
