*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/saucelabs.robot
Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/annotate.robot
Resource  plone/app/robotframework/speak.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Run keywords  Plone test setup
Test Teardown  Run keywords  Plone test teardown

*** Keywords ***

Add fading dot
    [Arguments]  ${locator}  ${number}
    ${dot} =  Add dot  ${locator}  ${number}  display=none
    Update element style  ${dot}  -moz-transform  scale(4)
    Update element style  ${dot}  display  block
    Update element style  ${dot}  -moz-transition  all 1s
    Update element style  ${dot}  -moz-transform  scale(1)
    Sleep  1s
    [return]  ${dot}

Add spoken note
    [Arguments]  ${locator}  ${message}  ${position}=${EMPTY}
    ${note} =  Add note  ${locator}  ${message}
    ...        display=none  position=${position}
    Speak  ${message}
    Update element style  ${note}  opacity  0
    Update element style  ${note}  display  block
    Update element style  ${note}  -moz-transition  opacity 1s
    Update element style  ${note}  opacity  1
    Sleep  2s
    [return]  ${note}

*** Test Cases ***

Introducing Mr. Roboto
    [Tags]  non-critical
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
    Sleep  0.5s

    ${dot} =  Add fading dot  user-name  1
    ${note} =  Add spoken note  user-name  This is me.  position=bottom
    Capture and crop page screenshot  robot-me.png
    ...    user-name  ${dot}  ${note}
    Remove elements  ${dot}  ${note}

    ${dot} =  Add fading dot  portaltab-index_html  2
    ${note} =  Add spoken note  portaltab-index_html  This is my home,
    ...        position=bottom
    Capture and crop page screenshot  robot-home.png
    ...    portaltab-index_html  ${dot}  ${note}
    Remove elements  ${dot}  ${note}

    ${dot} =  Add fading dot  content  3
    ${note} =  Add spoken note  portal-footer  and here's all my stuff.
    ...        position=top
    Capture and crop page screenshot  robot-content.png
    ...    content  ${dot}  ${note}
    Remove elements  ${dot}  ${note}

    ${dot} =  Add fading dot  portal-logo  4
    ${note} =  Add spoken note  portal-logo  Plone is my best friend,
    ...        position=bottom
    Capture and crop page screenshot  robot-logo.png
    ...    portal-logo  ${dot}  ${note}
    Remove elements  ${dot}  ${note}


    Speak  but I love you all.
    Sleep  2s
    Speak  Please, don't break my builds.
    Sleep  4s
    Speak  'asta la vistaa.
    Sleep  3s

    ${dot} =  Add pointer  user-name
    Sleep  0.5s
    Click element  user-name
    Sleep  0.5s
    Remove element  ${dot}
    ${dot} =  Add pointer  personaltools-logout
    Capture and crop page screenshot  robot-logout.png
    ...    portal-personaltools  portal-searchbox  ${dot}
    Sleep  0.5s
    Disable autologin
    Click link  Log out
    Sleep  4s
