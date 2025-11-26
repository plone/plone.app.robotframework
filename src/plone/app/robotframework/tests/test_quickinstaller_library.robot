# Start a single robot test
#
# Start the server
# WSGI_SERVER_HOST=localhost WSGI_SERVER_PORT=50003 robot-server plone.app.robotframework.testing.PLONE_ROBOT_TESTING
#
# Start the test
# WSGI_SERVER_HOST=localhost WSGI_SERVER_PORT=50003 robot src/plone/app/robotframework/tests/test_quickinstaller_library.robot
#
# or run: ROBOT_BROWSER=headlesschrome zope-testrunner --test-path=src --all -t test_quickinstaller_library.robot
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

*** Test Cases ***

Some default product is activated
    Given 'plone.app.users' is activated
      and 'plone.session' is not activated

*** Keywords ***

'${product}' is activated
    Product is activated    ${product}

'${product}' is not activated
    Run keyword and expect error    *    Product is activated    ${product}
