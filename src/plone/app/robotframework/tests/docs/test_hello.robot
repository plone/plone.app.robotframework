*** Settings ***

Test Tags  wip-not_in_docs

Resource    plone/app/robotframework/browser.robot

Library    Remote    ${PLONE_URL}/RobotRemote

Test Setup    Run Keywords    Plone test setup
Test Teardown    Run keywords     Plone test teardown

*** Test Cases ***

Plone is installed
    Go to  ${PLONE_URL}
    Get Element count    :text("Powered by Plone"):visible    >    0
