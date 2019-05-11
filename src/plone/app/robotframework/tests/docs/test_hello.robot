*** Settings ***

Force Tags  wip-not_in_docs

Resource  plone/app/robotframework/saucelabs.robot
Resource  plone/app/robotframework/selenium.robot

Test Setup  Run keywords  Plone test setup
Test Teardown  Run keywords  Plone test teardown

*** Test Cases ***

Plone is installed
    Go to  ${PLONE_URL}
    Page should contain  Powered by Plone
