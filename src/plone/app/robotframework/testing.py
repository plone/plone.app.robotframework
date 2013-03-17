# -*- coding: utf-8 -*-
from plone.app.robotframework import RemoteKeywordsLibrary
from plone.app.testing import ploneSite
from plone.testing import Layer


class SimplePublicationLayer(Layer):

    def setUp(self):
        with ploneSite() as portal:
            portal.portal_workflow.setDefaultChain(
                'simple_publication_workflow')

    def tearDown(self):
        with ploneSite() as portal:
            portal.portal_workflow.setDefaultChain('')

SIMPLE_PUBLICATION_FIXTURE = SimplePublicationLayer()


class RemoteKeywordsLibraryLayer(Layer):

    def setUp(self):
        with ploneSite() as portal:
            portal._setObject('RemoteKeywordsLibrary', RemoteKeywordsLibrary())

    def tearDown(self):
        with ploneSite() as portal:
            portal._delObject('RemoteKeywordsLibrary')

REMOTE_LIBRARY_FIXTURE = RemoteKeywordsLibraryLayer()
