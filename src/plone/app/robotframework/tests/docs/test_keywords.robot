*** Settings ***

Test Tags  wip-not_in_docs

Resource    plone/app/robotframework/browser.robot

Library    Remote    ${PLONE_URL}/RobotRemote

Test Setup    Run Keywords    Plone test setup
Test Teardown    Run keywords     Plone test teardown

# disable headless mode for browser
# set the variable BROWSER to chrome or firefox
# *** Variables ***
# ${BROWSER}    chrome

*** Variables ***

${ADMIN_ROLE}    Site Administrator

*** Test Cases ***

Site Administrator can access control panel
    Given I'm logged in as a '${ADMIN_ROLE}'
     When I open the personal menu
     Then I see the Site Setup -link

*** Keywords ***

I'm logged in as a '${ROLE}'
    Enable autologin as    ${ROLE}
    Go to    ${PLONE_URL}

I open the personal menu
    # Note: There is a key word "Open User Menu" as well.
    Click    //a[@id="personaltools-menulink"]
    Wait For Elements State    //ul[@id="collapse-personaltools"]    visible

I see the Site Setup -link
    Wait For Elements State    //a[@id="personaltools-plone_setup"]    visible