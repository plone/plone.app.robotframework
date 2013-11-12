*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/saucelabs.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open SauceLabs test browser
Test Teardown  Run keywords  Report test status  Close all browsers

*** Test cases ***

Test create content
    Enable autologin as  Contributor
    Create content  type=Document  id=example-document  title=Example document
    Go to  ${PLONE_URL}/example-document
    Page should contain  Example document

Test create content with custom id
    Enable autologin as  Contributor
    Create content  type=Document  id=example  title=Example document
    Go to  ${PLONE_URL}/example
    Page should contain  Example document

Test uid to url resolving
    Enable autologin as  Contributor
    ${uid} =  Create content  type=Document  id=example-document
    ...  title=Example document
    ${url} =  UID to URL  ${uid}
    Go to  ${url}
    Page should contain  Example document

Test fire transition
    Enable autologin as  Contributor  Reviewer
    ${uid} =  Create content  type=Document  id=example-document
    ...  title=Example document
    Fire transition  ${uid}  publish
    Disable autologin
    Go to  ${PLONE_URL}/example-document
    Page should contain  Example document
