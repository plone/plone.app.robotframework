Installing RIDE (Robot Framework IDE)
=====================================

[ride]-extras will create a script to start RIDE, the IDE for Robot Framework,
but it can be launched only explicitly with a compatible system python with
wxPython 2.8.x installed.

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
       plone.app.robotframework[ride]

If you can get RIDE running, you should select its *Run*-tab, change the value
of *Execution Profile* to *custom script*, and click Browser*-button to select
*bin/robot* from the buildout directory. Running RIDE using bin/robot* will
enable test isolation to work when running tests from RIDE.

If you want to place a breakpoint you can use the ``Comment`` keyword with
argument ``PAUSE``. RIDE will stop and let you step through your test.
