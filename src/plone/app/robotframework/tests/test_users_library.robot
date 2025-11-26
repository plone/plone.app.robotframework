# Start a single robot test
#
# Start the server
# WSGI_SERVER_HOST=localhost WSGI_SERVER_PORT=50003 robot-server plone.app.robotframework.testing.PLONE_ROBOT_TESTING
#
# Start the test
# WSGI_SERVER_HOST=localhost WSGI_SERVER_PORT=50003 robot src/plone/app/robotframework/tests/test_users_library.robot
#
# or run: ROBOT_BROWSER=headlesschrome zope-testrunner --test-path=src --all -t test_users_library.robot
#
*** Settings ***

Resource    plone/app/robotframework/browser.robot

Library    Remote    ${PLONE_URL}/RobotRemote

Test Setup    Run Keywords    Plone test setup
Test Teardown    Run keywords     Plone test teardown

# disable headless mode for browser
# set the variable BROWSER to chrome or firefox
# *** Variables ***
# ${BROWSER}    chrome
#
*** Test Cases ***

Test user creation and login as created user
    Enable autologin as    Manager
    Create user    johndoe    password=secret123    username=John Doe
    Disable autologin
    Log in    johndoe    secret123

    Get Element count    :text("You are now logged in"):visible    >    0
    Get Element count    :text("johndoe"):visible    >    0

Test user creation with roles as args
    Enable autologin as    Manager
    Create user    siteadmin    Contributor  Reviewer  Site Administrator
    Disable autologin
    Log in    siteadmin    siteadmin
    Go to   ${PLONE_URL}

    Get Element count    :text("siteadmin"):visible    >    0
    Get Element count    :text("Manage portlets"):visible    >    0

Test user creation with roles as kwarg
    Enable autologin as    Manager
    @{roles} =  Create list    Contributor    Reviewer    Site Administrator
    Create user    siteadmin    roles=@{roles}
    Log in    siteadmin    siteadmin
    Go to   ${PLONE_URL}

    Get Element count    :text("siteadmin"):visible    >    0
    Get Element count    :text("Manage portlets"):visible    >    0

*** Keywords ***

Log in
    [Documentation]  Log in to the site as ${userid} using ${password}. There
    ...              is no guarantee of where in the site you are once this is
    ...              done. (You are responsible for knowing where you are and
    ...              where you want to be)
    [Arguments]  ${userid}  ${password}
    Go to    ${PLONE_URL}/login_form
    Type Text    //input[@name="__ac_name"]    ${userid}
    Type Text    //input[@name="__ac_password"]    ${password}
    Click    //button[@name="buttons.login"]
