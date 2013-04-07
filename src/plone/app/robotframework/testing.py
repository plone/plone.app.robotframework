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
    ploneSite
)
from plone.testing import (
    z2,
    Layer
)
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


LIVESEARCH_ROBOT_TESTING = FunctionalTesting(
    bases=(LIVESEARCH_FIXTURE, z2.ZSERVER_FIXTURE),
    name="LiveSearch:Robot"
)

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
