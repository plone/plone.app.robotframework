*** Settings ***

Force Tags  wip-not_in_docs

Resource  plone/app/robotframework/saucelabs.robot
Resource  plone/app/robotframework/selenium.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Run keywords  Plone test setup
Test Teardown  Run keywords  Plone test teardown

*** Variables ***

${ADMIN_ROLE}  Site Administrator

*** Test Cases ***

Site Administrator can access control panel
    Given I'm logged in as a '${ADMIN_ROLE}'
     When I open the personal menu
     Then I see the Site Setup -link

*** Keywords ***

I'm logged in as a '${ROLE}'
    Enable autologin as  ${ROLE}
    Go to  ${PLONE_URL}

I open the personal menu
    # Note: There is a key word "Open User Menu" as well.
    Click link  css=#portal-personaltools a
    Wait Until Element Is Visible  css=#portal-personaltools .plone-toolbar-submenu-header

I see the Site Setup -link
    Element should be visible  css=#personaltools-plone_setup
