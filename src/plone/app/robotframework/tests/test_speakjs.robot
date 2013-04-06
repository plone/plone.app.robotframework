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

Add fading dot
    [Arguments]  ${locator}
    ${dot} =  Add dot  ${locator}  display=none
    Update element style  ${dot}  opacity  0.5
    Update element style  ${dot}  display  block
    Sleep  0.5s
    [return]  ${dot}

Add fading note
    [Arguments]  ${locator}  ${sleep}  ${message}
    ...          ${background}=white
    ...          ${color}=black
    ...          ${border}=1px solid black
    ${note} =  Add note  ${locator}  ${sleep}  ${message}
    ...                  ${background}  ${color}  ${border}
    ...                  display=none
    Update element style  ${note}  background  -moz-linear-gradient(top, rgba(235,241,246,1) 0%, rgba(171,211,238,1) 50%, rgba(137,195,235,1) 51%, rgba(213,235,251,1) 100%)
    Update element style  ${note}  border  none
    Update element style  ${note}  box-shadow   0 0 10px black
    Update element style  ${note}  -moz-transform  rotate(90deg)
    Update element style  ${note}  opacity  0
    Update element style  ${note}  -moz-transition  all 1s
    Update element style  ${note}  display  block
    Update element style  ${note}  -moz-transform  rotate(0deg)
    Update element style  ${note}  opacity  1
    Sleep  1s
    [return]  ${note}

Show note with dot
    [Arguments]  ${locator}  ${sleep}  ${message}
    ...          ${background}=white
    ...          ${color}=black
    ...          ${border}=1px solid black
    ${dot} =  Add fading dot  ${locator}
    Speak  ${message}
    ${note} =  Add fading note  ${locator}  ${sleep}  ${message}
    ...                         ${background}  ${color}  ${border}
    Sleep  2s
    Remove element  ${dot}
    Remove element  ${note}

*** Test cases ***

Say something
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

    Show note with dot  jquery=#user-name  2s  This is me.
    Show note with dot  jquery=#portaltab-index_html  2s  This is my home,
    Show note with dot  jquery=#content  2s  and here's all my stuff.
    Show note with dot  jquery=#portal-logo  2s  Plone is my friend,

    Speak  and so are U.
    Sleep  2s
    Speak  I love you all.
    Sleep  2s
    Speak  Please, don't break my builds.
    Sleep  2s
    Speak  'asta la vistaa.
    Sleep  3s

    ${dot} =  Add fading dot  jquery=#user-name
    Sleep  0.5s
    Click element  css=#user-name
    Sleep  0.5s
    Remove element  ${dot}
    Add fading dot  jquery=#personaltools-logout
    Sleep  0.5s
    Disable autologin
    Click link  Log out
    Sleep  4s
