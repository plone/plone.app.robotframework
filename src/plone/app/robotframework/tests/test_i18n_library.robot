*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/saucelabs.robot
Resource  plone/app/robotframework/selenium.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Run keywords  Plone test setup
Test Teardown  Run keywords  Plone test teardown

*** Test Cases ***

Test translation
    Set default language  fi
    ${msg} =  Translate  Edit
    Should be equal  ${msg}  Muokkaa
