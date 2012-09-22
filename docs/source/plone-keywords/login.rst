==============================================================================
Plone Login/Logout Keywords
==============================================================================

Login
-----

Log in (with username and password)::

    Log in to the site as <username>.  There is no guarantee of where in the
    site you are once this is done. (You are responsible for knowing where
    you are and where you want to be)

Log in as site owner::

    Log in as the SITE_OWNER provided by plone.app.testing, with all the rights
    and privileges of that user.

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
