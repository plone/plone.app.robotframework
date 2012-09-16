# -*- coding: utf-8 -*-
"""Python unittest / zope.testrunner compatible test suite for 'plone.act'
to be used in testing 'plone.act' with 'robotsuite'."""

# XXX: Do not use this as an example to use 'robotsuite' in your own
# tests. Please, refer to our 'readthedocs'-documentation instead.

import unittest

from plone.testing import layered

from plone.app.testing import PLONE_ZSERVER

import robotsuite


def dummy(*args, **kwargs):
    pass


def testSetUp():
    """Neutralizes 'Zope2ServerLibrary' before running every test, because
    'PLONE_ZSERVER'-layer from 'plone.app.testing' takes care of starting and
    stopping the server and cleaning up the test database between tests."""

    import plone.act
    plone.act.Zope2ServerLibrary.start_zope_server = dummy
    plone.act.Zope2ServerLibrary.stop_zope_server = dummy
    plone.act.Zope2ServerLibrary.zodb_setup = dummy
    plone.act.Zope2ServerLibrary.zodb_teardown = dummy


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite("acceptance-tests",
                                          setUp=testSetUp),
                layer=PLONE_ZSERVER),
    ])
    return suite
