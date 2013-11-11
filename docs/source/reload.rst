Auto-reload code with robot-server
==================================

[reload]-extras will make ``robot-server`` to detect filesystem changes under
``./src`` and reload the test layer when a change is detected.

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
       plone.app.robotframework[reload]


If you added the ``reload``-extras to the ``plone.app.robotframework`` egg and
there is no ``src`` directory in your buildout (such as when you are using the
buildout of a specific product), robot-server will complain and fail to start.
In this case, use the ``--reload-paths`` option on the command line to tell it where it
should watch for changes, e.g.:

.. code-block:: bash

   $ bin/robot-server --reload-path <mypath> my.product.testing.MY_PRODUCT_ROBOT_TESTING
