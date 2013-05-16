*** Settings ***

Library  Collections
Library  plone.app.robotframework.Zope2Server

Resource  selenium.robot

*** Keywords ***

Setup Plone site
    [Arguments]  ${zope_layer_dotted_name}  @{extra_layers_dotted_names}

    Start Zope server  ${zope_layer_dotted_name}
    :FOR  ${extra_layer_dotted_name}  IN  @{extra_layers_dotted_names}
    \  Amend Zope server  ${extra_layer_dotted_name}
    Set Zope layer  ${zope_layer_dotted_name}

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
