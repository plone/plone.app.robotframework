# -*- coding: utf-8 -*-
"""Test layers required to run plone.app.robotframework tests.

This module is located below tests directory to avoid confusing it with any
re-usable resources of plone.app.robotframework.
"""
import os
from Acquisition import aq_base
from Products.MailHost.interfaces import IMailHost

from plone.app.testing import (
    PloneSandboxLayer,
    applyProfile,
    PLONE_FIXTURE,
    FunctionalTesting,
    ploneSite
)
from plone.testing import (
    z2,
    Layer
)
import sys
from zope.component import getSiteManager
from zope.configuration import xmlconfig
from plone.app.robotframework import (
    QuickInstaller,
    AutoLogin,
    RemoteLibraryLayer
)

import pkg_resources

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
        from Products.CMFPlone.tests.utils import MockMailHost
        with ploneSite() as portal:
            portal.email_from_address = 'noreply@example.com'
            portal.email_from_name = 'Plone Site'
            portal._original_MailHost = portal.MailHost
            portal.MailHost = mailhost = MockMailHost('MailHost')
            portal.MailHost.smtp_host = 'localhost'
            sm = getSiteManager(context=portal)
            sm.unregisterUtility(provided=IMailHost)
            sm.registerUtility(mailhost, provided=IMailHost)

    def tearDown(self):
        with ploneSite() as portal:
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
    libraries=(AutoLogin, QuickInstaller),
    name="RemoteLibraryBundle:RobotRemote"
)

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
            return BuiltIn().get_variable_value('${%s}' % name, [])
        else:
            candidates = os.environ.get(name, '').split(',')
            return filter(bool, [s.strip() for s in candidates])

    def setUpZope(self, app, configurationContext):

        import collective.usermanual
        xmlconfig.file('configure.zcml', collective.usermanual,
                       context=configurationContext)

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
               SIMPLE_PUBLICATION_FIXTURE,
               REMOTE_LIBRARY_BUNDLE_FIXTURE,
               z2.ZSERVER_FIXTURE),
        name="SpeakJS:Robot"
    )
