from plone.testing.zope import WSGI_SERVER_FIXTURE

import pkg_resources


ZOPE_HOST = WSGI_SERVER_FIXTURE.host
ZOPE_PORT = WSGI_SERVER_FIXTURE.port

CMFPLONE_VERSION = pkg_resources.get_distribution("Products.CMFPlone").version

if CMFPLONE_VERSION.startswith("4."):
    CMFPLONE_SELECTORS = "selectors/cmfplone43.robot"
elif CMFPLONE_VERSION.startswith("5."):
    CMFPLONE_SELECTORS = "selectors/cmfplone50.robot"
elif CMFPLONE_VERSION.startswith("6."):
    CMFPLONE_SELECTORS = "selectors/cmfplone60.robot"
