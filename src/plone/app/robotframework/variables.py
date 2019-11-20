# coding=utf-8
import os
import pkg_resources


try:
    from plone.testing.zope import WSGI_SERVER_FIXTURE
except ImportError:
    # Plone 5.1 compatibility, remove in Plone 6
    from plone.testing.z2 import ZSERVER_FIXTURE as WSGI_SERVER_FIXTURE

ZOPE_HOST = WSGI_SERVER_FIXTURE.host
ZOPE_PORT = WSGI_SERVER_FIXTURE.port

CMFPLONE_VERSION = pkg_resources.get_distribution('Products.CMFPlone').version
if CMFPLONE_VERSION.startswith('4.'):
    CMFPLONE_SELECTORS = 'selectors/cmfplone43.robot'
elif CMFPLONE_VERSION.startswith('5.'):
    CMFPLONE_SELECTORS = 'selectors/cmfplone50.robot'
