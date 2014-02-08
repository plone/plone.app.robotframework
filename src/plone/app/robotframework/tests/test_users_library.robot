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

    Element should contain  id=user-name  johndoe
