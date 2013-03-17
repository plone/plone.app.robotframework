# -*- coding: utf-8 -*-
"""Test layers required to run plone.app.robotframework tests.

This module is located below tests directory to avoid confusing it with any
re-usable resources of plone.app.robotframework.

"""
from plone.app.testing import (
    PloneSandboxLayer,
    applyProfile,
    PLONE_FIXTURE,
    FunctionalTesting,
)
from plone.testing import z2
from zope.configuration import xmlconfig
from plone.app.robotframework.testing import (
    SIMPLE_PUBLICATION_FIXTURE,
    REMOTE_LIBRARY_FIXTURE
)


class LiveSearchLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import plone.app.robotframework.tests
        xmlconfig.file(
            '_profiles.zcml',
            plone.app.robotframework.tests,
            context=configurationContext
        )

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'plone.app.robotframework.tests:content')

LIVESEARCH_FIXTURE = LiveSearchLayer()

LIVESEARCH_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(LIVESEARCH_FIXTURE, z2.ZSERVER_FIXTURE),
    name="LiveSearch:Functional"
)

REMOTE_LIBRARY_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PLONE_FIXTURE, SIMPLE_PUBLICATION_FIXTURE,
           REMOTE_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE),
    name="RemoteKeywordsLibrary:Functional"
)
