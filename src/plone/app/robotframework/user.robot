*** Keywords *****************************************************************

a logged in site administrator
  [Documentation]  Log in to the site as site administrator. There is no
  ...              guarantee of where in the site you are once this is done.
  Enable autologin as  Site Administrator

a logged in manager
  Enable autologin as  Manager
  [Documentation]  Log in to the site as manager. There is no guarantee of
  ...              where in the site you are once this is done.
