==============================================================================
Plone Browser Keywords
==============================================================================

Start browser and wake plone up::

    Start browser and wake plone up

        [Arguments]  ${ZOPE_LAYER_DOTTED_NAME}

        Start Zope Server  ${ZOPE_LAYER_DOTTED_NAME}
        Zodb setup
        Set Selenium timeout  15s
        Set Selenium implicit wait  1s

        ${previous}  Register keyword to run on failure  Close Browser
        Wait until keyword succeeds  2min  3s  Access plone
        Register keyword to run on failure  ${previous}


        Wait until keyword succeeds  30s  1s  Log in as site owner
        Log out
        Zodb teardown

Close browser and selenium server::

    Close browser and selenium server
        Close browser
        Stop Zope Server