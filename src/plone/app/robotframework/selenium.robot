*** Settings ***

# We set run_on_failure to Nothing because anything else interferes with
# 'Wait until keyword succeeds', interpreting an initial failure as complete failure,
# instead of waiting for a successful retry.
Library  Selenium2Library  timeout=${SELENIUM_TIMEOUT}
...                        implicit_wait=${SELENIUM_IMPLICIT_WAIT}
...                        run_on_failure=${SELENIUM2LIBRARY_RUN_ON_FAILURE}

Resource  variables.robot
Resource  ${CMFPLONE_SELECTORS}

*** Variables ***

${SELENIUM_IMPLICIT_WAIT}  0.5
${SELENIUM_TIMEOUT}  30
${SELENIUM_RUN_ON_FAILURE}  Capture Page Screenshot
${SELENIUM2LIBRARY_RUN_ON_FAILURE}  No operation

${BROWSER}  Firefox
${REMOTE_URL}
${FF_PROFILE_DIR}
${DESIRED_CAPABILITIES}

*** Keywords ***

# ----------------------------------------------------------------------------
# Browser
# ----------------------------------------------------------------------------

Open test browser
    Open browser  ${START_URL}  ${BROWSER}
    ...           remote_url=${REMOTE_URL}
    ...           desired_capabilities=${DESIRED_CAPABILITIES}
    ...           ff_profile_dir=${FF_PROFILE_DIR}

Wait until location is
    [Arguments]  ${expected_url}
    ${TIMEOUT} =  Get Selenium timeout
    ${IMPLICIT_WAIT} =  Get Selenium implicit wait
    Wait until keyword succeeds  ${TIMEOUT}  ${IMPLICIT_WAIT}
    ...                          Location should be  ${expected_url}

Plone Test Setup
    Open SauceLabs test browser
    Run keyword and ignore error  Set window size  4096  4096

Plone Test Teardown
    Run Keyword If Test Failed  ${SELENIUM_RUN_ON_FAILURE}
    Report test status
    Close all browsers

Capture page screenshot and log source
    Capture page screenshot
    Log source

# ----------------------------------------------------------------------------
# Elements
# ----------------------------------------------------------------------------

Possibly stale element should not be visible
    [Arguments]  ${locator}
    @{value} =  Run keyword and ignore error
    ...         Element should not be visible  ${locator}
    Should be equal  @{value}[0]  PASS

Element should not remain visible
    [Documentation]  Due to the internals of Selenium2Library, a disappearing
    ...              element may rise StaleElementReferenceException (element
    ...              disappears between it's located and inspected). This
    ...              keyword is a workaround that tries again until success.
    [Arguments]  ${locator}
    ${TIMEOUT} =  Get Selenium timeout
    ${IMPLICIT_WAIT} =  Get Selenium implicit wait
    Wait until keyword succeeds  ${TIMEOUT}  ${IMPLICIT_WAIT}
    ...                          Possibly stale element should not be visible
    ...                          ${locator}

Possibly stale element should become visible
    [Arguments]  ${locator}
    @{value} =  Run keyword and ignore error
    ...         Element should be visible  ${locator}
    Should be equal  @{value}[0]  PASS

Element should become visible
    [Documentation]  Due to the internals of Selenium2Library, an appearing
    ...              element may rise StaleElementReferenceException (element
    ...              disappears between it's located and inspected). This
    ...              keyword is a workaround that tries again until success.
    [Arguments]  ${locator}
    ${TIMEOUT} =  Get Selenium timeout
    ${IMPLICIT_WAIT} =  Get Selenium implicit wait
    Wait until keyword succeeds  ${TIMEOUT}  ${IMPLICIT_WAIT}
    ...                          Possibly stale element should become visible
    ...                          ${locator}

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
    Input text  ${locator}  ${text}
    ${value} =  Get value  ${locator}
    Should be equal  ${text}  ${value}
