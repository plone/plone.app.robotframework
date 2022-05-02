from zope.globalrequest import getRequest
from zope.interface import alsoProvides


try:
    from plone.protect.interfaces import IDisableCSRFProtection
except ImportError:
    from zope.interface import Interface
    class IDisableCSRFProtection(Interface):
        pass


def disableCSRFProtection():
    alsoProvides(getRequest(), IDisableCSRFProtection)