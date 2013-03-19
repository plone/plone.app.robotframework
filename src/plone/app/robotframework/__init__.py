# -*- coding: utf-8 -*-
# Stand-alone Python keyword libraries
from plone.app.robotframework.server import Zope2ServerLibrary
from plone.app.robotframework.saucelabs import SauceLabsLibrary
from plone.app.robotframework.keywords import DebuggingLibrary
from plone.app.robotframework.keywords import LayoutMathLibrary

# Remote Python libraries
from plone.app.robotframework.quickinstaller import QuickInstallerRemoteLibrary
from plone.app.robotframework.autologin import AutoLoginRemoteLibrary

# Generic remote Python library layer
from plone.app.robotframework.remote import RemoteLibraryLayer
