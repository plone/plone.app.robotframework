import os
import pkg_resources

try:
    from plone.testing.z2 import DEFAULT_ZSERVER_PORT
except ImportError:
    # DEFAULT_ZSERVER_PORT is not defined until plone.testing == 4.0.8
    DEFAULT_ZSERVER_PORT = 55001

# plone.testing checks environment to allow overriding DEFAULT_ZSERVER_PORT
ZSERVER_PORT = os.environ.get('ZSERVER_PORT', DEFAULT_ZSERVER_PORT)

# Allow specifying HOST and PORT through environment variables for instance,
# if tests should go through a proxy
ZOPE_HOST = os.environ.get('ZOPE_HOST', 'localhost')
ZOPE_PORT = os.environ.get('ZOPE_PORT', ZSERVER_PORT)

CMFPLONE_VERSION = pkg_resources.get_distribution('Products.CMFPlone').version
if CMFPLONE_VERSION.startswith('4.'):
    CMFPLONE_SELECTORS = 'selectors/cmfplone43.robot'
elif CMFPLONE_VERSION.startswith('5.'):
    CMFPLONE_SELECTORS = 'selectors/cmfplone50.robot'

