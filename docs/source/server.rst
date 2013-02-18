Speed up your test writing with ACT-server
==========================================

**plone.act** comes with a special console script ``act_server``, which starts
up a Plone site with a given
`plone.app.testing <http://pypi.python.org/pypi/plone.app.testing/>`_
testing layer set up.

This will save time when writing new robot tests, because you can try out your
unfinished test over and over again without the usual time consuming
setup/teardown of testing layers between every test.

Install ``act_server`` with support for the developed product with a buildout
part::
    [buildout]
    ...
    parts += act_server
    versions = versions

    extensions = mr.developer
    sources = sources
    auto-checkout = plone.act

    [sources]
    plone.act = git git://github.com/plone/plone.act

    [versions]
    plone.app.testing = 4.2.2

    [act_server]
    recipe = zc.recipe.egg
    eggs =
        plone.act
        my.product

After buildout, start ``act_server`` with::

    $ bin/act_server my.product.testing.MY_PRODUCT_FUNCTIONAL_TESTING

And run tests with ``pybot`` and ``act_server`` test isolation support with::

    $ bin/pybot --listener plone.act.server.ZODB src/my/product/tests/robot_tests.txt
