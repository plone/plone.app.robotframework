from plone.protect.interfaces import IDisableCSRFProtection
from zope.globalrequest import getRequest
from zope.interface import alsoProvides


def disableCSRFProtection():
    alsoProvides(getRequest(), IDisableCSRFProtection)
