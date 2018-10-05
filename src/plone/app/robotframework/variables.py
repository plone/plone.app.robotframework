from plone.testing.z2 import ZSERVER_FIXTURE
import os
import pkg_resources

ZOPE_HOST = ZSERVER_FIXTURE.host
ZOPE_PORT = ZSERVER_FIXTURE.port

CMFPLONE_VERSION = pkg_resources.get_distribution('Products.CMFPlone').version
if CMFPLONE_VERSION.startswith('4.'):
    CMFPLONE_SELECTORS = 'selectors/cmfplone43.robot'
elif CMFPLONE_VERSION.startswith('5.'):
    CMFPLONE_SELECTORS = 'selectors/cmfplone50.robot'
