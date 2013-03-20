*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/saucelabs.robot

Test Setup  Open SauceLabs test browse
Test Teardown  Run keywords  Report test status  Close all browsers

*** Test cases ***

Check close on click off form
    Go to homepage
    Click Link  Contact
    Overlay should open
    Page should contain  Contact form
    Click Element  css=#exposeMask
    Overlay should close on same page
    Page should not contain  Contact form

Check close on click close
    Goto homepage
    Click Link  Contact
    Overlay should open
    Page should contain  Contact form
    Click Element  css=div.overlay div.close
    Overlay should close on same page
    Page should not contain  Contact form

*** Keywords ***

Overlay should open
    Wait until keyword succeeds  1  5  Element Should Be Visible  id=exposeMask
    Element should be visible  css=div.overlay
    Element should be visible  css=div.overlay div.close

Overlay should close on same page
    Wait until keyword succeeds  1  5  Element Should Not Be Visible  id=exposeMask
    Wait until keyword succeeds  1  5  Page should not contain element  css=div.overlay
