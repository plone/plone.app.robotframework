# -*- coding: utf-8 -*-

# Stand-alone Python keyword libraries
from plone.app.robotframework.server import Zope2Server
from plone.app.robotframework.saucelabs import SauceLabs
from plone.app.robotframework.keywords import Debugging
from plone.app.robotframework.keywords import LayoutMath
from plone.app.robotframework.annotate import Annotate

# Remote Python libraries
from plone.app.robotframework.server import Zope2ServerRemote
from plone.app.robotframework.i18n import I18N
from plone.app.robotframework.autologin import AutoLogin
from plone.app.robotframework.mailhost import MockMailHost
from plone.app.robotframework.ploneapi import PloneAPI
from plone.app.robotframework.portalsetup import PortalSetup
from plone.app.robotframework.quickinstaller import QuickInstaller

# Generic remote Python library layer
from plone.app.robotframework.remote import RemoteLibraryLayer

# Pybot listener for calling Robot Server from pybot
from plone.app.robotframework.server import RobotListener

# Robot Plone fixture
from plone.app.robotframework.testing import PLONE_ROBOT_FIXTURE
