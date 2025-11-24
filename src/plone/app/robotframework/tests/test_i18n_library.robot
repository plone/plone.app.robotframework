# Start a single robot test
#
# Start the server
# WSGI_SERVER_HOST=localhost WSGI_SERVER_PORT=50003 robot-server plone.app.robotframework.testing.PLONE_ROBOT_TESTING
#
# Start the test
# WSGI_SERVER_HOST=localhost WSGI_SERVER_PORT=50003 robot src/plone/app/robotframework/tests/test_i18n_library.robot
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

Test translation
    Set default language  fi
    ${msg} =  Translate  Edit
    Should be equal  ${msg}  Muokkaa
