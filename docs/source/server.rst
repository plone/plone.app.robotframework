Speed up your test writing with robot-server
============================================

**plone.app.robotframework** comes with a special console script
``robot-server``, which starts up a Plone site with a given `plone.app.testing
<http://pypi.python.org/pypi/plone.app.testing/>`_ testing layer set up.

This will save time when writing new robot tests, because you can try out your
unfinished test over and over again without the usual time consuming
setup/teardown of testing layers between every test.

Install ``robot-server`` and its counter part ``robot`` with support for the
developed product with a buildout part::

    [buildout]
    ...
    parts += robot

    [robot]
    recipe = zc.recipe.egg
    eggs =
        ${test:eggs}
        plone.app.robotframework
    scripts =
        robot-server
        robot

After buildout, start ``robot-server`` with::

    $ bin/robot-server my.product.testing.MY_PRODUCT_FUNCTIONAL_TESTING

And run tests with ``robot`` and ``robot-server`` test isolation support with::

    $ bin/robot src/my/product/tests/test_something.robot
