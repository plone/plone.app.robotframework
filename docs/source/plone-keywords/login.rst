==============================================================================
Plone Login/Logout Keywords
==============================================================================

Login
-----

Log in (with username and password)::

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

Log in as site owner::

    Log in as site owner
        ${name} =  Get site owner name
        ${password} =  Get site owner password
        Log in  ${name}  ${password}

Log in as ${username} with role(s) ${roles}::

    Log in as ${username} with role(s) ${roles}

        [Arguments]  ${userid}  ${roles}
        XXX: We need a generic way to login with a user that has one or more roles.

.. warning::

    - Do we need to be able to assign multiple roles at once?

    - Do we need to assign roles to arbitray users or is it sufficient if we
      always assign those roles to the test user?

Logout
------

Log out::

    Log out
        Go to  ${PLONE_URL}/logout
        Page should contain  logged out
