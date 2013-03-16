from Products.CMFCore.utils import getToolByName


def setupContent(context):
    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('plone-app-robotframework-content.txt') is None:
        return
    setup_tool = context.getSetupTool()
    portal = getToolByName(setup_tool, 'portal_url').getPortalObject()
    portal.invokeFactory(type_name="Document", id='welcome-to-plone',
            title="Welcome to Plone")
    portal.invokeFactory(type_name="Document", id='a-livesearch-test-page',
            title="A livesearch test page")
    portal.invokeFactory(type_name="Folder", id='a-livesearch-test-folder',
            title="A livesearch test folder")
    folder = portal.get('a-livesearch-test-folder')
    folder.invokeFactory(type_name="Document", id='a-livesearch-test-page-1',
            title="A livesearch test page 1")
    folder.invokeFactory(type_name="Document", id='a-livesearch-test-page-2',
            title="A livesearch test page 2")
