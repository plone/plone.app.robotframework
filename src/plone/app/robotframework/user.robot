*** Keywords *****************************************************************

a logged in site administrator
  [Documentation]  Log in to the site as site administrator. There is no
  ...              guarantee of where in the site you are once this is done.
  Enable autologin as  Site Administrator

a logged in manager
  Enable autologin as  Manager
  [Documentation]  Log in to the site as manager. There is no guarantee of
  ...              where in the site you are once this is done.

a logged in test user
  [Documentation]  Log in to the site as test user. This test user is
  ...              equivalent to the TEST_USER_NAME in plone.app.testing.
  ...              There is no guarantee of where in the site you are once
  ...              this is done.
  Enable autologin as  Member  Contributor
  Set autologin username  ${TEST_USER_NAME}

a logged in site owner
  Enable autologin as  Member
  Set autologin username  ${SITE_OWNER_NAME}
