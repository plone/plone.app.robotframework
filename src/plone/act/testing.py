# -*- coding: utf-8 -*-
from plone.app.testing import (
    PloneSandboxLayer,
    applyProfile,
    PLONE_FIXTURE,
    FunctionalTesting
)
from plone.testing import z2
from zope.configuration import xmlconfig
from plone.act import RemoteKeywordsLibrary


class LiveSearchLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import plone.act
        xmlconfig.file(
            'profiles.zcml',
            plone.act,
            context=configurationContext
        )

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'plone.act:content')

LIVESEARCH_FIXTURE = LiveSearchLayer()

LIVESEARCH_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(LIVESEARCH_FIXTURE, z2.ZSERVER_FIXTURE),
    name="LiveSearch:Functional"
)


class RemoteKeywordsLibraryLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpPloneSite(self, portal):
        portal._setObject("RemoteKeywordsLibrary", RemoteKeywordsLibrary())

    def tearDownPloneSite(self, portal):
        portal._delObject("RemoteKeywordsLibrary")


REMOTE_LIBRARY_FIXTURE = RemoteKeywordsLibraryLayer()

REMOTE_LIBRARY_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(REMOTE_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE),
    name="RemoteKeywordsLibrary:Functional"
)
