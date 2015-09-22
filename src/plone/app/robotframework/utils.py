from zope.interface import alsoProvides
from zope.globalrequest import getRequest

try:
    from plone.protect.interfaces import IDisableCSRFProtection
except ImportError:
    from zope.interface import Interface
    class IDisableCSRFProtection(Interface):
        pass


def disableCSRFProtection():
    alsoProvides(getRequest(), IDisableCSRFProtection)