# -*- coding: utf-8 -*-
from plone.app.robotframework import (
    RemoteKeywordsLibrary,
    AutoLoginLibrary
)
from plone.app.testing import (
    PLONE_FIXTURE,
    ploneSite
)
from plone.testing import Layer


class SimplePublicationLayer(Layer):

    defaultBases = (PLONE_FIXTURE,)

    def setUp(self):
        with ploneSite() as portal:
            portal.portal_workflow.setDefaultChain(
                'simple_publication_workflow')

    def tearDown(self):
        with ploneSite() as portal:
            portal.portal_workflow.setDefaultChain('')

SIMPLE_PUBLICATION_FIXTURE = SimplePublicationLayer()


class RemoteKeywordsLibraryLayer(Layer):

    defaultBases = (PLONE_FIXTURE,)

    def setUp(self):
        with ploneSite() as portal:
            portal._setObject('RemoteKeywordsLibrary', RemoteKeywordsLibrary())

    def tearDown(self):
        with ploneSite() as portal:
            portal._delObject('RemoteKeywordsLibrary')

REMOTE_LIBRARY_FIXTURE = RemoteKeywordsLibraryLayer()


class AutoLoginLibraryLayer(Layer):

    defaultBases = (PLONE_FIXTURE,)

    def setUp(self):
        with ploneSite() as portal:
            portal._setObject('AutoLoginLibrary', AutoLoginLibrary())

    def tearDown(self):
        with ploneSite() as portal:
            portal._delObject('AutoLoginLibrary')

AUTOLOGIN_LIBRARY_FIXTURE = AutoLoginLibraryLayer()
