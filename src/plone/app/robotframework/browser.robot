*** Settings ***

# This browser.robot setups Robot tests with Playwright via robotframework-browser.
# This browser.robot cannot be used with selenium.robot, saucelabs.robot or keywords.robot.

# Requires initialization::
#
# $ bin/rfbrowser init
#
# Creates video and trace with ROBOT_TRACE=true
# Pauses execution on error with ROBOT_DEBUG=true
# Run browser as headless with ROBOT_HEADLESS=true
# Is backwards compatible with ROBOT_BROWESR=headless[browsername]
#
# Traces can be viewed with
#
# $ bin/rfbrowser -F parts/test/*/*/tracing show-trace
#
# Keywords: https://marketsquare.github.io/robotframework-browser/Browser.html

Library  Browser  run_on_failure=${BROWSER_RUN_ON_FAILURE}

Resource  variables.robot
Resource  ${CMFPLONE_SELECTORS}

*** Variables ***

${BROWSER_RUN_ON_FAILURE}  Take Screenshot

${BROWSER}  headlesschromium

${DEBUG}  false
${HEADLESS}  false
${TRACE}  false
${TRACING}  ${OUTPUT_DIR}/tracing

*** Keywords ***

# ----------------------------------------------------------------------------
# Browser
# ----------------------------------------------------------------------------

# https://marketsquare.github.io/robotframework-browser/Browser.html#New%20Persistent%20Context

Configure Test Browser
    ${DEBUG}=     Set Variable If     "${DEBUG}".lower() in ["1", "on", "true", "yes"]  ${TRUE}  ${FALSE}
    ${TRACE}=     Set Variable If     "${TRACE}".lower() in ["1", "on", "true", "yes"]  ${TRUE}  ${FALSE}
    ${HEADLESS}=  Set Variable If     "${HEADLESS}".lower() in ["1", "on", "true", "yes"]  ${TRUE}  ${FALSE}
    ${HEADLESS}=  Set Variable if     "${BROWSER}".startswith("headless")  ${TRUE}  ${HEADLESS}
    ${HEADLESS}=  Set Variable If     ${TRACE}  ${FALSE}  ${HEADLESS}
    ${HEADLESS}=  Set Variable If     ${DEBUG}  ${FALSE}  ${HEADLESS}
    ${BROWSER}=   Set Variable if     "${BROWSER}".startswith("headless")  ${BROWSER[len("headless"):]}  ${BROWSER}
    ${BROWSER}=   Set Variable if     "${BROWSER}" == "chrome"  chromium  ${BROWSER}
    ${VIDEO}=     Create dictionary   dir  ${OUTPUT_DIR}/video

    Set Suite Variable  ${BROWSER}    ${BROWSER}
    Set Suite Variable  ${DEBUG}      ${DEBUG}
    Set Suite Variable  ${HEADLESS}   ${HEADLESS}
    Set Suite Variable  ${TRACE}      ${TRACE}
    Set Suite Variable  ${VIDEO}      ${VIDEO}

Open Test Browser
    Configure Test Browser
    Run Keyword If  ${DEBUG}
    ...    Open browser
    ...        url=${START_URL}
    ...        browser=${BROWSER}
    ...    ELSE IF  ${TRACE}
    ...    New persistent context
    ...        url=${START_URL}
    ...        browser=${BROWSER}
    ...        tracing=${TRACING}
    ...        headless=${HEADLESS}
    ...        recordVideo=${VIDEO}
    ...    ELSE
    ...    New persistent context
    ...        url=${START_URL}
    ...        browser=${BROWSER}
    ...        headless=${HEADLESS}

Plone Test Setup
    Open Test Browser

Plone Test Teardown
    Run Keyword If Test Failed  ${BROWSER_RUN_ON_FAILURE}
    Run Keyword If  ${TRACE}  Sleep  1s
    Close browser

Capture page screenshot
    Take screenshot

Capture page screenshot and log source
    Take screenshot
    ${source}=  Get page source
    Log  ${source}
