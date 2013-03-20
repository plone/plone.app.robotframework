*** Settings ***

Library  plone.app.robotframework.Zope2ServerLibrary

Resource  selenium.robot

*** Keywords ***

Start browser and wake Plone up
    [Arguments]  ${ZOPE_LAYER_DOTTED_NAME}

    Start Zope server  ${ZOPE_LAYER_DOTTED_NAME}
    Zodb setup

    ${previous} =  Register keyword to run on failure  Close Browser
    Wait until keyword succeeds  2min  3s  Access plone
    Register keyword to run on failure  ${previous}

Access Plone
    Open test browser
    Go to homepage

Close browser, teardown zodb, and stop selenium server
    Close browser
    Zodb teardown
    Stop Zope server
