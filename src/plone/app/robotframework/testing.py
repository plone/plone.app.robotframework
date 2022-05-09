"""Test layers required to run plone.app.robotframework tests."""
from Acquisition import aq_base
from OFS.Application import AppInitializer
from plone.app.robotframework.autologin import AutoLogin
from plone.app.robotframework.content import Content
from plone.app.robotframework.genericsetup import GenericSetup
from plone.app.robotframework.i18n import I18N
from plone.app.robotframework.mailhost import MockMailHost
from plone.app.robotframework.quickinstaller import QuickInstaller
from plone.app.robotframework.remote import RemoteLibraryLayer
from plone.app.robotframework.server import Zope2ServerRemote
from plone.app.robotframework.users import Users
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import ploneSite
from plone.testing import Layer
from plone.testing import zope as zope_testing
from plone.testing.zope import WSGIServer
from plone.testing.zope import WSGI_SERVER_FIXTURE
from Products.MailHost.interfaces import IMailHost
from robot.libraries.BuiltIn import BuiltIn
from webtest.http import StopableWSGIServer
from zope.component import getSiteManager
from zope.configuration import xmlconfig

import os
import pkg_resources
import sys


try:
    pkg_resources.get_distribution("collective.js.speakjs")
except pkg_resources.DistributionNotFound:
    HAS_SPEAKJS = False
else:
    HAS_SPEAKJS = True


class SimplePublicationLayer(Layer):
    defaultBases = (PLONE_FIXTURE,)

    def setUp(self):
        with ploneSite() as portal:
            applyProfile(portal, "plone.app.contenttypes:default")
            portal.portal_workflow.setDefaultChain("simple_publication_workflow")

    def tearDown(self):
        with ploneSite() as portal:
            portal.portal_workflow.setDefaultChain("")


SIMPLE_PUBLICATION_FIXTURE = SimplePublicationLayer()


class SimplePublicationWithTypesLayer(Layer):

    defaultBases = (SIMPLE_PUBLICATION_FIXTURE,)

    def setUp(self):
        with ploneSite() as portal:
            applyProfile(portal, "plone.app.contenttypes:default")


SIMPLE_PUBLICATION_WITH_TYPES_FIXTURE = SimplePublicationLayer()


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
            portal.email_from_address = "noreply@example.com"
            portal.email_from_name = "Plone Site"
            portal._original_MailHost = portal.MailHost
            portal.MailHost = mailhost = utils.MockMailHost("MailHost")
            portal.MailHost.smtp_host = "localhost"
            sm = getSiteManager(context=portal)
            sm.unregisterUtility(provided=IMailHost)
            sm.registerUtility(mailhost, provided=IMailHost)

    def tearDown(self):
        with ploneSite() as portal:
            _o_mailhost = getattr(portal, "_original_MailHost", None)
            if _o_mailhost:
                portal.MailHost = portal._original_MailHost
                sm = getSiteManager(context=portal)
                sm.unregisterUtility(provided=IMailHost)
                sm.registerUtility(
                    aq_base(portal._original_MailHost), provided=IMailHost
                )


MOCK_MAILHOST_FIXTURE = MockMailHostLayer()


AUTOLOGIN_LIBRARY_FIXTURE = RemoteLibraryLayer(
    bases=(PLONE_FIXTURE,),
    libraries=(AutoLogin,),
    name="AutoLoginRemoteLibrary:RobotRemote",
)

REMOTE_LIBRARY_BUNDLE_FIXTURE = RemoteLibraryLayer(
    bases=(PLONE_FIXTURE,),
    libraries=(
        AutoLogin,
        QuickInstaller,
        GenericSetup,
        Content,
        Users,
        I18N,
        MockMailHost,
        Zope2ServerRemote,
    ),
    name="RemoteLibraryBundle:RobotRemote",
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
    "RobotRemote",
    (
        AutoLogin,
        QuickInstaller,
        GenericSetup,
        Content,
        Users,
        I18N,
        MockMailHost,
        Zope2ServerRemote,
    ),
    {"__doc__": "Robot Framework remote library", "id": "RobotRemote"},
)()

REMOTE_LIBRARY_ROBOT_TESTING = FunctionalTesting(
    bases=(
        SIMPLE_PUBLICATION_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        WSGI_SERVER_FIXTURE,
    ),
    name="RemoteLibrary:Robot",
)

AUTOLOGIN_ROBOT_TESTING = FunctionalTesting(
    bases=(AUTOLOGIN_LIBRARY_FIXTURE, WSGI_SERVER_FIXTURE),
    name="AutoLogin:Robot",
)

SIMPLE_PUBLICATION_ROBOT_TESTING = FunctionalTesting(
    bases=(
        SIMPLE_PUBLICATION_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        WSGI_SERVER_FIXTURE,
    ),
    name="SimplePublication:Robot",
)

SIMPLE_PUBLICATION_WITH_TYPES_ROBOT_TESTING = FunctionalTesting(
    bases=(
        SIMPLE_PUBLICATION_WITH_TYPES_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        WSGI_SERVER_FIXTURE,
    ),
    name="SimplePublicationWithTypes:Robot",
)


class PloneRobotFixture(PloneSandboxLayer):
    defaultBases = (
        SIMPLE_PUBLICATION_FIXTURE,
        MOCK_MAILHOST_FIXTURE,
    )

    def _get_robot_variable(self, name):
        """Return robot list variable either from robot instance or
        from ROBOT_-prefixed environment variable
        """
        if getattr(BuiltIn(), "_context", None) is not None:
            value = BuiltIn().get_variable_value("${%s}" % name, [])
            if isinstance(value, str) or isinstance(value, str):
                return value.split(",")
            else:
                return value
        else:
            candidates = os.environ.get(name, "").split(",")
            return filter(bool, [s.strip() for s in candidates])

    def setUpZope(self, app, configurationContext):

        # This installs the VHM in the Zope root, so we can have VHM support too
        AppInitializer(app).install_virtual_hosting()

        for locales in self._get_robot_variable("REGISTER_TRANSLATIONS"):
            if locales and os.path.isdir(locales):
                from zope.i18n.zcml import registerTranslations

                registerTranslations(configurationContext, locales)
                self["state"].append(locales)

        for name in self._get_robot_variable("META_PACKAGES"):
            if name not in sys.modules:
                __import__(name)
            package = sys.modules[name]
            xmlconfig.file("meta.zcml", package, context=configurationContext)
            self["state"].append(name)

        for name in self._get_robot_variable("CONFIGURE_PACKAGES"):
            if name not in sys.modules:
                __import__(name)
            package = sys.modules[name]
            xmlconfig.file("configure.zcml", package, context=configurationContext)
            self["state"].append(name)

        for name in self._get_robot_variable("OVERRIDE_PACKAGES"):
            if name not in sys.modules:
                __import__(name)
            package = sys.modules[name]
            xmlconfig.includeOverrides(
                configurationContext, "overrides.zcml", package=package
            )
            self["state"].append(name)

        for name in self._get_robot_variable("INSTALL_PRODUCTS"):
            if name not in sys.modules:
                __import__(name)
            zope_testing.installProduct(app, name)
            self["state"].append(name)

    def setUpPloneSite(self, portal):
        for name in self._get_robot_variable("APPLY_PROFILES"):
            self.applyProfile(portal, name)
            self["state"].append(name)

    def setUp(self):
        self["state"] = []
        super().setUp()

        class Value:
            def __repr__(self, x):
                return str(bool(x))

            def __nonzero__(x):
                return self.get("state", []) != (
                    self._get_robot_variable("REGISTER_TRANSLATIONS")
                    + self._get_robot_variable("META_PACKAGES")
                    + self._get_robot_variable("CONFIGURE_PACKAGES")
                    + self._get_robot_variable("OVERRIDE_PACKAGES")
                    + self._get_robot_variable("INSTALL_PRODUCTS")
                    + self._get_robot_variable("APPLY_PROFILES")
                )

        self["dirty"] = Value()


PLONE_ROBOT_FIXTURE = PloneRobotFixture()

PLONE_ROBOT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(
        PLONE_ROBOT_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
    ),
    name="PloneRobot:Integration",
)

PLONE_ROBOT_TESTING = FunctionalTesting(
    bases=(
        PLONE_ROBOT_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        WSGI_SERVER_FIXTURE,
    ),
    name="Plone:Robot",
)


class WSGIServerSingleThreaded(WSGIServer):

    def setUpServer(self):
        """Create a single threaded WSGI server instance and save it in self.server.
        """
        app = self.make_wsgi_app()
        kwargs = {'clear_untrusted_proxy_headers': False,
                  'threads': 1}
        if self.host is not None:
            kwargs['host'] = self.host
        if self.port is not None:
            kwargs['port'] = int(self.port)
        self.server = StopableWSGIServer.create(app, **kwargs)
        # If we dynamically set the host/port, we want to reset it to localhost
        # Otherwise this will depend on, for example, the local network setup
        if self.host in (None, '0.0.0.0', '127.0.0.1', 'localhost'):
            self.server.effective_host = 'localhost'
        # Refresh the hostname and port in case we dynamically picked them
        self['host'] = self.host = self.server.effective_host
        self['port'] = self.port = int(self.server.effective_port)



WSGI_SERVER_SINGLE_THREADED_FIXTURE = WSGIServerSingleThreaded()


VOLTO_ROBOT_TESTING = FunctionalTesting(
    bases=(
        PLONE_ROBOT_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        WSGI_SERVER_SINGLE_THREADED_FIXTURE,
    ),
    name="Volto:Robot",
)


if HAS_SPEAKJS:

    class SpeakJSLayer(Layer):

        defaultBases = (PLONE_FIXTURE,)

        def setUp(self):
            import collective.js.speakjs

            xmlconfig.file(
                "configure.zcml",
                collective.js.speakjs,
                context=self["configurationContext"],
            )

            with ploneSite() as portal:
                applyProfile(portal, "collective.js.speakjs:default")

    SPEAKJS_FIXTURE = SpeakJSLayer()

    SPEAKJS_ROBOT_TESTING = FunctionalTesting(
        bases=(
            SPEAKJS_FIXTURE,
            MOCK_MAILHOST_FIXTURE,
            SIMPLE_PUBLICATION_FIXTURE,
            REMOTE_LIBRARY_BUNDLE_FIXTURE,
            WSGI_SERVER_FIXTURE,
        ),
        name="SpeakJS:Robot",
    )
