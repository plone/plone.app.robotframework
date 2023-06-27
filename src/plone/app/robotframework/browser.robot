*** Settings ***

# This browser.robot setups Robot tests with Playwright via robotframework-browser.
# This browser.robot cannot be used with selenium.robot, saucelabs.robot or keywords.robot.

# Requires initialization::
#
# $ bin/rfbrowser init
#
# Creates video and trace with ROBOT_DEBUG=true
# 
# Traces can be viewed with
#
# $ bin/rfbrowser -F parts/test/*/*/tracing show-trace
#

# https://marketsquare.github.io/robotframework-browser/Browser.html#Importing

Library  Browser  run_on_failure=${BROWSER_RUN_ON_FAILURE}

Resource  variables.robot
Resource  ${CMFPLONE_SELECTORS}

*** Variables ***

${BROWSER_RUN_ON_FAILURE}  Take Screenshot

${BROWSER}  chromium

${ÐEBUG}
${TRACING}  ${OUTPUT_DIR}/tracing

*** Keywords ***

# ----------------------------------------------------------------------------
# Browser
# ----------------------------------------------------------------------------

# https://marketsquare.github.io/robotframework-browser/Browser.html#New%20Persistent%20Context

Open Test Browser
    ${record_video}  Create dictionary   dir  ${OUTPUT_DIR}/video
    Run Keyword If  "${DEBUG}".lower() == "true"
    ...    New persistent context
    ...        url=${START_URL}
    ...        browser=${BROWSER}
    ...        tracing=${TRACING}
    ...        recordVideo=${record_video}
    ...    ELSE
    ...    New persistent context
    ...        url=${START_URL}
    ...        browser=${BROWSER}

Plone Test Setup
    Open Test Browser

Plone Test Teardown
    Run Keyword If Test Failed  ${BROWSER_RUN_ON_FAILURE}
    Run Keyword If  "${DEBUG}".lower() == "true"  Sleep  1s
    Close browser

Capture page screenshot
    Take screenshot

Capture page screenshot and log source
    Take screenshot
    ${source}=  Get page source
    Log source  ${source}
