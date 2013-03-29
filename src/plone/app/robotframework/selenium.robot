*** Settings ***

Library  Selenium2Library  timeout=${SELENIUM_TIMEOUT}
...                        implicit_wait=${SELENIUM_IMPLICIT_WAIT}

Resource  variables.robot

*** Variables ***

${SELENIUM_IMPLICIT_WAIT}  0.5
${SELENIUM_TIMEOUT}  10

${BROWSER}  Firefox
${REMOTE_URL}
${DESIRED_CAPABILITIES}

*** Keywords ***

# ----------------------------------------------------------------------------
# Browser
# ----------------------------------------------------------------------------

Open test browser
    Open browser  ${PLONE_URL}  ${BROWSER}
    ...           remote_url=${REMOTE_URL}
    ...           desired_capabilities=${DESIRED_CAPABILITIES}

Wait until location is
    [Arguments]  ${expected_url}
    ${TIMEOUT} =  Get Selenium timeout
    ${IMPLICIT_WAIT} =  Get Selenium implicit wait
    Wait until keyword succeeds  ${TIMEOUT}  ${IMPLICIT_WAIT}
    ...                          Location should be  ${expected_url}

# ----------------------------------------------------------------------------
# Forms
# ----------------------------------------------------------------------------

Input text for sure
    [Documentation]  Locate input element by ${locator} and enter the given
    ...              ${text}. Validate that the text has been entered.
    ...              Retry until the set Selenium timeout. (The purpose of
    ...              this keyword is to fix random input issues on slow test
    ...              machines.)
    [Arguments]  ${locator}  ${text}
    ${TIMEOUT} =  Get Selenium timeout
    ${IMPLICIT_WAIT} =  Get Selenium implicit wait
    Wait until keyword succeeds  ${TIMEOUT}  ${IMPLICIT_WAIT}
    ...                          Input text and validate  ${locator}  ${text}

Input text and validate
    [Documentation]  Locate input element by ${locator} and enter the given
    ...              ${text}. Validate that the text has been entered.
    [Arguments]  ${locator}  ${text}
    Focus  ${locator}
    Input text  ${locator}  ${text}
    ${value} =  Get value  ${locator}
    Should be equal  ${text}  ${value}
