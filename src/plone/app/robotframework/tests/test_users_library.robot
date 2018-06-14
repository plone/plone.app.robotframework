*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/saucelabs.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open SauceLabs test browser
Test Teardown  Run keywords  Report test status  Close all browsers

*** Test Cases ***

Test user creation and login as created user
    Enable autologin as  Manager
    Create user  johndoe  password=secret  username=John Doe
    Disable autologin
    Log in  johndoe  secret

    Page should contain  You are now logged in
    Page should contain  johndoe

Test user creation with roles as args
    Enable autologin as  Manager
    Create user  siteadmin  Contributor  Reviewer  Site Administrator
    Disable autologin
    Log in  siteadmin  siteadmin
    Go to homepage
    
    Page should contain  siteadmin
    Page should contain  Manage portlets

Test user creation with roles as kwarg
    Enable autologin as  Manager
    @{roles} =  Create list  Contributor  Reviewer  Site Administrator
    Create user  siteadmin  roles=@{roles}
    Log in  siteadmin  siteadmin
    Go to homepage
    
    Page should contain  siteadmin
    Page should contain  Manage portlets
