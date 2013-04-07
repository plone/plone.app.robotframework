*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/saucelabs.robot
Resource  plone/app/robotframework/annotate.robot
Resource  plone/app/robotframework/speak.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open SauceLabs test browser
Test Teardown  Run keywords  Report test status  Close all browsers

*** Keywords ***

Add fading note
    [Arguments]  ${locator}  ${message}
    ${note} =  Add note  ${locator}  ${message}
    Update element style  ${note}  opacity  0
    Update element style  ${note}  display  block
    Update element style  ${note}  -moz-transition  opacity 1s
    Update element style  ${note}  opacity  1
    Sleep  1s
    [return]  ${note}

Show note with dot
    [Arguments]  ${locator}  ${message}
    ${dot} =  Add dot  ${locator}
    Speak  ${message}
    ${note} =  Add fading note  ${locator}  ${message}
    Sleep  2s
    Remove element  ${dot}
    Remove element  ${note}

*** Test cases ***

Introducing Mr. Roboto
    Go to  ${PLONE_URL}
    Sleep  1s

    Update element style  visual-portal-wrapper  -moz-transition  all 2s
    Update element style  visual-portal-wrapper  -moz-transform  rotate(180deg) scale(0)
    Update element style  visual-portal-wrapper  margin-top  50%
    Sleep  3s

    Speak  Don't be afaid.
    Sleep  2s

    Speak  I am now controlling the transmission.
    Sleep  4s

    Speak  I am mister roboto
    Sleep  2s

    Update element style  visual-portal-wrapper  -moz-transform  scale(1) rotate(0deg)
    Update element style  visual-portal-wrapper  margin-top  0%

    Speak  Welcome to Plone
    Sleep  2s

    Enable autologin as  Site Administrator
    Set autologin username   Mr. Roboto

    Go to  ${PLONE_URL}

    Show note with dot  jquery=#user-name  This is me.
    Show note with dot  jquery=#portaltab-index_html  This is my home,
    Show note with dot  jquery=#content  and here's all my stuff.
    Show note with dot  jquery=#portal-logo  Plone is my friend,

    Speak  and so are U.
    Sleep  2s
    Speak  I love you all.
    Sleep  2s
    Speak  Please, don't break my builds.
    Sleep  2s
    Speak  'asta la vistaa.
    Sleep  3s

    ${dot} =  Add dot  jquery=#user-name
    Sleep  0.5s
    Click element  css=#user-name
    Sleep  0.5s
    Remove element  ${dot}
    Add dot  jquery=#personaltools-logout
    Sleep  0.5s
    Disable autologin
    Click link  Log out
    Sleep  4s
