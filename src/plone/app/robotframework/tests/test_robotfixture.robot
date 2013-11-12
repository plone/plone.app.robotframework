*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/saucelabs.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open SauceLabs test browser
Test Teardown  Run keywords  Report test status  Close all browsers

*** Test Cases ***

Session refresh support should be activated
    Product is activated  plone.session
