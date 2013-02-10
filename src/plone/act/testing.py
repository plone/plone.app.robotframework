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
        remote_keywords = RemoteKeywords(portal)
        remote_library = RemoteKeywordsLibrary(remote_keywords)
        portal._setObject("RemoteKeywordsLibrary", remote_library)

    def tearDownPloneSite(self, portal):
        portal._delObject("RemoteKeywordsLibrary")


REMOTE_LIBRARY_FIXTURE = RemoteKeywordsLibraryLayer()

REMOTE_LIBRARY_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(REMOTE_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE),
    name="RemoteKeywordsLibrary:Functional"
)


class RemoteKeywords(object):

    def __init__(self, portal):
        self._portal = portal

    def product_has_been_activated(self, product_name):
        from Products.CMFCore.utils import getToolByName
        quickinstaller = getToolByName(self._portal, "portal_quickinstaller")
        assert quickinstaller.isProductInstalled(product_name),\
            "Product '%s' was not installed." % product_name
