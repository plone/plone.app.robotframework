*** Comments ***
# Start a single robot test
#
# Start the server
# WSGI_SERVER_HOST=localhost WSGI_SERVER_PORT=50003 robot-server plone.app.robotframework.tests.test_robotfixture.PLONE_ROBOT_TESTING
#
# Start the test
# WSGI_SERVER_HOST=localhost WSGI_SERVER_PORT=50003 robot src/plone/app/robotframework/tests/test_robotfixture.robot
#
# or run: ROBOT_BROWSER=headlesschrome zope-testrunner --test-path=src --all -t test_robotfixtures.robot
#


*** Settings ***
Resource            plone/app/robotframework/browser.robot
Library             Remote    ${PLONE_URL}/RobotRemote

Test Setup          Run Keywords    Plone test setup
Test Teardown       Run keywords    Plone test teardown
# disable headless mode for browser
# set the variable BROWSER to chrome or firefox
# *** Variables ***
# ${BROWSER}    chrome


*** Test Cases ***
Session refresh support should be activated
    Product is activated    plone.session
