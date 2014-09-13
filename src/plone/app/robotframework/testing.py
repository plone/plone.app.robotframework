# -*- coding: utf-8 -*-
"""Test layers required to run plone.app.robotframework tests.

This module is located below tests directory to avoid confusing it with any
re-usable resources of plone.app.robotframework.
"""
from Acquisition import aq_base
from Products.MailHost.interfaces import IMailHost
from plone.app.robotframework.autologin import AutoLogin
from plone.app.robotframework.content import Content
from plone.app.robotframework.genericsetup import GenericSetup
from plone.app.robotframework.i18n import I18N
from plone.app.robotframework.mailhost import MockMailHost
from plone.app.robotframework.quickinstaller import QuickInstaller
from plone.app.robotframework.remote import RemoteLibraryLayer
from plone.app.robotframework.server import Zope2ServerRemote
from plone.app.robotframework.users import Users
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import ploneSite
from plone.testing import Layer
from plone.testing import z2
from zope.component import getSiteManager
from zope.configuration import xmlconfig
import os
import pkg_resources
import sys

try:
    pkg_resources.get_distribution('collective.js.speakjs')
except pkg_resources.DistributionNotFound:
    HAS_SPEAKJS = False
else:
    HAS_SPEAKJS = True
from robot.libraries.BuiltIn import BuiltIn


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


class MockMailHostLayer(Layer):
    """Layer for setting up a MockMailHost to store all sent messages as
    strings into a list at portal.MailHost.messages
    """
    defaultBases = (PLONE_FIXTURE,)

    def setUp(self):
        # Note: CMFPlone can be imported safely only when a certain
        # zope.testing-set environment variable is in place.
        from Products.CMFPlone.tests import utils
        with ploneSite() as portal:
            portal.email_from_address = 'noreply@example.com'
            portal.email_from_name = 'Plone Site'
            portal._original_MailHost = portal.MailHost
            portal.MailHost = mailhost = utils.MockMailHost('MailHost')
            portal.MailHost.smtp_host = 'localhost'
            sm = getSiteManager(context=portal)
            sm.unregisterUtility(provided=IMailHost)
            sm.registerUtility(mailhost, provided=IMailHost)

    def tearDown(self):
        with ploneSite() as portal:
            _o_mailhost = getattr(portal, '_original_MailHost', None)
            if _o_mailhost:
                portal.MailHost = portal._original_MailHost
                sm = getSiteManager(context=portal)
                sm.unregisterUtility(provided=IMailHost)
                sm.registerUtility(aq_base(portal._original_MailHost),
                                   provided=IMailHost)

MOCK_MAILHOST_FIXTURE = MockMailHostLayer()


AUTOLOGIN_LIBRARY_FIXTURE = RemoteLibraryLayer(
    bases=(PLONE_FIXTURE,),
    libraries=(AutoLogin,),
    name="AutoLoginRemoteLibrary:RobotRemote"
)

REMOTE_LIBRARY_BUNDLE_FIXTURE = RemoteLibraryLayer(
    bases=(PLONE_FIXTURE,),
    libraries=(AutoLogin, QuickInstaller, GenericSetup,
               Content, Users, I18N, MockMailHost,
               Zope2ServerRemote),
    name="RemoteLibraryBundle:RobotRemote"
)

#
# The following default remote library instance can be registered to function
# as a Robot Framework remote library with collective.monkeypatcher:
#
# <monkey:patch
#     description="Enable Robot Framework remote library"
#     class="Products.CMFPlone.Portal.PloneSite"
#     original="RobotRemote"
#     replacement="plone.app.robotframework.testing.RobotRemote"
#     ignoreOriginal="true"
#     />
#

RobotRemote = type(
    'RobotRemote',
    (AutoLogin, QuickInstaller, GenericSetup,
     Content, Users, I18N, MockMailHost,
     Zope2ServerRemote),
    {'__doc__': 'Robot Framework remote library',
                'id': 'RobotRemote'})()

REMOTE_LIBRARY_ROBOT_TESTING = FunctionalTesting(
    bases=(SIMPLE_PUBLICATION_FIXTURE,
           REMOTE_LIBRARY_BUNDLE_FIXTURE,
           z2.ZSERVER_FIXTURE),
    name="RemoteLibrary:Robot"
)

AUTOLOGIN_ROBOT_TESTING = FunctionalTesting(
    bases=(AUTOLOGIN_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE),
    name="AutoLogin:Robot"
)

SIMPLE_PUBLICATION_ROBOT_TESTING = FunctionalTesting(
    bases=(SIMPLE_PUBLICATION_FIXTURE,
           REMOTE_LIBRARY_BUNDLE_FIXTURE,
           z2.ZSERVER_FIXTURE),
    name="SimplePublication:Robot"
)


class PloneRobotFixture(PloneSandboxLayer):
    defaultBases = (SIMPLE_PUBLICATION_FIXTURE,
                    MOCK_MAILHOST_FIXTURE,
                    REMOTE_LIBRARY_BUNDLE_FIXTURE)

    def _get_robot_variable(self, name):
        """Return robot list variable either from robot instance or
        from ROBOT_-prefixed environment variable
        """
        if getattr(BuiltIn(), '_context', None) is not None:
            value = BuiltIn().get_variable_value('${%s}' % name, [])
            if isinstance(value, str) or isinstance(value, unicode):
                return value.split(',')
            else:
                return value
        else:
            candidates = os.environ.get(name, '').split(',')
            return filter(bool, [s.strip() for s in candidates])

    def setUpZope(self, app, configurationContext):
        for locales in self._get_robot_variable('REGISTER_TRANSLATIONS'):
            if locales and os.path.isdir(locales):
                from zope.i18n.zcml import registerTranslations
                registerTranslations(configurationContext, locales)

        for name in self._get_robot_variable('META_PACKAGES'):
            if not name in sys.modules:
                __import__(name)
            package = sys.modules[name]
            xmlconfig.file('meta.zcml', package,
                           context=configurationContext)

        for name in self._get_robot_variable('CONFIGURE_PACKAGES'):
            if not name in sys.modules:
                __import__(name)
            package = sys.modules[name]
            xmlconfig.file('configure.zcml', package,
                           context=configurationContext)

        for name in self._get_robot_variable('OVERRIDE_PACKAGES'):
            if not name in sys.modules:
                __import__(name)
            package = sys.modules[name]
            xmlconfig.includeOverrides(
                configurationContext, 'overrides.zcml', package=package)

        for name in self._get_robot_variable('INSTALL_PRODUCTS'):
            if not name in sys.modules:
                __import__(name)
            z2.installProduct(app, name)

    def setUpPloneSite(self, portal):
        for name in self._get_robot_variable('APPLY_PROFILES'):
            self.applyProfile(portal, name)


PLONE_ROBOT_FIXTURE = PloneRobotFixture()

PLONE_ROBOT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONE_ROBOT_FIXTURE,),
    name="PloneRobot:Integration"
)

PLONE_ROBOT_TESTING = FunctionalTesting(
    bases=(PLONE_ROBOT_FIXTURE, z2.ZSERVER_FIXTURE),
    name="Plone:Robot"
)


if HAS_SPEAKJS:
    class SpeakJSLayer(Layer):

        defaultBases = (PLONE_FIXTURE,)

        def setUp(self):
            import collective.js.speakjs
            xmlconfig.file('configure.zcml', collective.js.speakjs,
                           context=self['configurationContext'])

            with ploneSite() as portal:
                applyProfile(portal, 'collective.js.speakjs:default')

    SPEAKJS_FIXTURE = SpeakJSLayer()

    SPEAKJS_ROBOT_TESTING = FunctionalTesting(
        bases=(SPEAKJS_FIXTURE,
               MOCK_MAILHOST_FIXTURE,
               SIMPLE_PUBLICATION_FIXTURE,
               REMOTE_LIBRARY_BUNDLE_FIXTURE,
               z2.ZSERVER_FIXTURE),
        name="SpeakJS:Robot"
    )
