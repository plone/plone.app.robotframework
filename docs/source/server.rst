Speed-up your test writing with ACT-server
==========================================

**plone.act** comes with a special console script ``act_server``, which starts
up a Plone site with a given
`plone.app.testing <http://pypi.python.org/pypi/plone.app.testing/>`_
testing layer set up.

This will save time, because you can write new tests without the usual time
consuming setup/teardown of testing layers.

Install ``act_server`` with support for the developed product with a buildout
part::

    [act_server]
    recipe = zc.recipe.egg
    eggs =
        plone.act
        my.product

Start ``act_server`` with::

    $ bin/act_server my.product.testing.MY_PRODUCT_FUNCTIONAL_TESTING

And run tests fast with ``pybot`` and ``act_server`` test isolation support
with::

    $ bin/pybot --listener plone.act.server.ZODB src/my/product/tests/robot_tests.txt
