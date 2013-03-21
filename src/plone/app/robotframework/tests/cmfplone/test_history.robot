*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/saucelabs.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Run keywords  Open SauceLabs test browser
Test Teardown  Run keywords  Report test status  Close all browsers

*** Test cases ***

Open history popup
    Enable autologin as  Contributor
    Go to homepage
    Add Page  History testing page
    Open history popup
    Element Should Be Visible  css=.pb-ajax #content-history
