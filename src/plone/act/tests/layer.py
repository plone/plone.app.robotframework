from plone.testing import z2, Layer
from plone.app.testing import PLONE_FIXTURE, FunctionalTesting, PLONE_SITE_ID, SITE_OWNER_NAME

class Populated(Layer):
    defaultBases = (PLONE_FIXTURE,)

    def setUp(self):
        with z2.zopeApp() as app:
            z2.login(app['acl_users'], SITE_OWNER_NAME)
            app[PLONE_SITE_ID].invokeFactory(type_name="Document", id='welcome-to-plone', title="Welcome to Plone")
            app[PLONE_SITE_ID].invokeFactory(type_name="Document", id='a-livesearch-test-page', title="A livesearch test page")
            app[PLONE_SITE_ID].invokeFactory(type_name="Folder", id='a-livesearch-test-folder', title="A livesearch test folder")
            folder = app[PLONE_SITE_ID].get('a-livesearch-test-folder')
            folder.invokeFactory(type_name="Document", id='a-livesearch-test-page-1', title="A livesearch test page 1")
            folder.invokeFactory(type_name="Document", id='a-livesearch-test-page-2', title="A livesearch test page 2")

POPULATED = Populated()

POPULATED_PLONEZSERVER             = FunctionalTesting(bases=(POPULATED, z2.ZSERVER_FIXTURE), name='Plone:PopulatedZServer')
