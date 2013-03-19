*** Settings ***

Library  Selenium2Library  timeout=${SELENIUM_TIMEOUT}
...                        implicit_wait=${SELENIUM_IMPLICIT_WAIT}

Resource  variables.robot

*** Variables ***

${SELENIUM_IMPLICIT_WAIT} =  0.5
${SELENIUM_TIMEOUT} =  10

${BROWSER} =  Firefox
${REMOTE_URL} =
${DESIRED_CAPABILITIES} =

*** Keywords ***

Open test browser
    Open browser  ${PLONE_URL}  ${BROWSER}
    ...           remote_url=${REMOTE_URL}
    ...           desired_capabilities=${DESIRED_CAPABILITIES}
