*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/saucelabs.robot

Library  Remote  ${PLONE_URL}/RobotRemoteLibrary

Test Setup  Run keywords  Open SauceLabs test browser
Test Teardown  Run keywords  Report test status  Close all browsers


*** Test cases ***

Test edit wizard tabs navigation
    Given the edit wizard form
     Then I am able to see wizard tabs
     When I click on Settings tab
     Then I see the current tab is changed correctly
      And current tab content is changed to Settings

*** Keywords ***

the edit wizard form
    Enable autologin as  Contributor  Editor
    Go to homepage
    Add Page  test edit wizard
    Go to  ${PLONE_URL}/test-edit-wizard/edit

I am able to see wizard tabs
    Element Should Be Visible  css=ul.formTabs

When I click on Settings tab
    Open wizard tab  Settings

Then I see the current tab is changed correctly
    Element Should Be Visible  css=ul.formTabs li.formTab:last-child a#fieldsetlegend-settings.selected

And current tab content is changed to Settings
    Page should contain  Exclude from navigation
