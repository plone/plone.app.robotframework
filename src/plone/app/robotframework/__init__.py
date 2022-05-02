# Stand-alone Python keyword libraries
# Load our patches.  Call it _patches to mark it as private.
from plone.app.robotframework import patches as _patches
from plone.app.robotframework.annotate import Annotate
from plone.app.robotframework.autologin import AutoLogin
from plone.app.robotframework.content import Content
from plone.app.robotframework.genericsetup import GenericSetup
from plone.app.robotframework.i18n import I18N
from plone.app.robotframework.keywords import Debugging
from plone.app.robotframework.keywords import LayoutMath
from plone.app.robotframework.mailhost import MockMailHost
from plone.app.robotframework.quickinstaller import QuickInstaller

# Generic remote Python library layer
from plone.app.robotframework.remote import RemoteLibraryLayer
from plone.app.robotframework.saucelabs import SauceLabs

# Pybot listener for calling Robot Server from pybot
# Remote Python libraries
from plone.app.robotframework.server import RobotListener
from plone.app.robotframework.server import Zope2Server
from plone.app.robotframework.server import Zope2ServerRemote

# Robot Plone fixture
from plone.app.robotframework.testing import PLONE_ROBOT_TESTING
from plone.app.robotframework.users import Users
