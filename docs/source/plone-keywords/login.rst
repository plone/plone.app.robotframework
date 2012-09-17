==============================================================================
Plone Login/Logout Keywords
==============================================================================

Log in::

    Log in
        [Arguments]  ${userid}  ${password}
        Go to  ${PLONE_URL}/login_form
        Page should contain element  __ac_name
        Input text  __ac_name  ${userid}
        Input text  __ac_password  ${password}
        Click Button  Log in
        Page should contain element  css=#user-name
        Go to  ${PLONE_URL}
        [Return]  True

Log out::

    Log out
        Go to  ${PLONE_URL}/logout
        Page should contain  logged out

Log in as site owner::

    Log in as site owner
        ${name} =  Get site owner name
        ${password} =  Get site owner password
        Log in  ${name}  ${password}

Access plone::

    Access plone
        Open browser  ${ZOPE_URL}  ${BROWSER}
        Goto homepage
        [Return]  True
