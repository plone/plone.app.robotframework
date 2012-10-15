import os

from plone.app.testing.interfaces import PLONE_SITE_ID

PORT = os.environ.get('ZSERVER_PORT', 55001)
SELENIUM_IMPLICIT_WAIT = os.environ.get('SELENIUM_IMPLICIT_WAIT', '5s')

ZOPE_URL = "http://localhost:%s" % PORT
PLONE_URL = "%s/%s" % (ZOPE_URL, PLONE_SITE_ID)
BROWSER = "Firefox"
REMOTE_URL = ""
DESIRED_CAPABILITIES = ""
TEST_FOLDER = "%s/acceptance-test-folder"
