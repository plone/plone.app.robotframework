*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/saucelabs.robot

Test setup  Open SauceLabs test browser
Test teardown  Run keywords  Report test status  Close all browsers

*** Test cases ***

Add document
    Login as site owner
    Add document  Test document
