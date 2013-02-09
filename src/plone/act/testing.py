from plone.app.testing import (
    PloneSandboxLayer,
    applyProfile,
    PLONE_FIXTURE,
    FunctionalTesting
)
from plone.testing import z2
from zope.configuration import xmlconfig


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
