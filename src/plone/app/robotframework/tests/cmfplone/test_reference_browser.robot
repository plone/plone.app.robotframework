*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/saucelabs.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Run keywords  Open SauceLabs test browser
Test Teardown  Run keywords  Report test status  Close all browsers

*** Test cases ***

Test related items field
    Given the edit wizard form categorization step
    Then I am able to select any particular content item as 'related'

*** Keywords ***

the edit wizard form categorization step
    Enable autologin as  Site Administrator
    Go to homepage
    Add Page  test reference browser widget
    Go to homepage
    Add Folder  test folder
    Add Page  test reference browser widget related
    Go to  ${PLONE_URL}/test-reference-browser-widget/edit
    Open wizard tab  Categorization

Then I am able to select any particular content item as 'related'
    Set Reference Browser Field Value  relatedItems  test folder  test reference browser widget related
