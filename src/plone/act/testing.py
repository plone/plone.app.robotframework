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


from Products.PluggableAuthService.plugins import DomainAuthHelper
from Products.PlonePAS.Extensions.Install import activatePluginInterfaces


class RemoteKeywords(object):

    def __init__(self, portal):
        self._portal = portal

    def product_has_been_activated(self, product_name):
        from Products.CMFCore.utils import getToolByName
        quickinstaller = getToolByName(self._portal, "portal_quickinstaller")
        assert quickinstaller.isProductInstalled(product_name),\
            "Product '%s' was not installed." % product_name

    def autologin_as(self, *args):
        """Adds and configures DomainAuthHelper PAS-plugin to login
        all anonymous users from localhost as a special *Remote User* with
        one or more given roles. Examples of use::

            Autologin as  Manager
            Autologin as  Site Administrator
            Autologin as  Member  Contributor

        """

        if "robot_login" in self._portal.acl_users.objectIds():
            self._portal.acl_users.robot_login._domain_map.clear()
        else:
            DomainAuthHelper.manage_addDomainAuthHelper(
                self._portal.acl_users, "robot_login")
            activatePluginInterfaces(self._portal, "robot_login")
        self._portal.acl_users.robot_login.manage_addMapping(
            match_type="equals", match_string="localhost", roles=args)
