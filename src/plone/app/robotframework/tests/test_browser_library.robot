*** Settings ***

Resource  plone/app/robotframework/browser.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Run keywords  Plone test setup
Test Teardown  Run keywords  Plone test teardown

*** Test Cases ***

Test create content
    Enable autologin as  Contributor
    Create content  type=Document  id=example-document  title=Example document
    Go to  ${PLONE_URL}/example-document
    Get text  h1  Should be  Example document
   
# https://marketsquare.github.io/robotframework-browser/Browser.html#Assertions
    