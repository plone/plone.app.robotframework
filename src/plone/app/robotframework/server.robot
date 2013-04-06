*** Settings ***

Library  plone.app.robotframework.Zope2Server

Resource  selenium.robot

*** Keywords ***

Setup Plone site
    [Arguments]  ${zope_layer_dotted_name}

    Start Zope server  ${zope_layer_dotted_name}
    Zodb setup

    ${previous} =  Register keyword to run on failure  Close Browser
    Wait until keyword succeeds  2min  3s  Browser can be opened
    Register keyword to run on failure  ${previous}

Browser can be opened
    Open test browser

Teardown Plone site
    Close all browsers
    Zodb teardown
    Stop Zope server
