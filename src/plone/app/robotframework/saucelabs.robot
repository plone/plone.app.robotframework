*** Settings ***

Resource  selenium.robot

Library  String
Library  plone.app.robotframework.SauceLabs

*** Variables ***

${BUILD_NUMBER}  manual
${SELENIUM_VERSION}  2.31.0
${SESSION_ID}

*** Keywords ***

Open SauceLabs test browser
    [Documentation]  Open test browser at SauceLabs. The initial test name is
    ...              composed of suite name and test name, but colons (:) are
    ...              removed, because *Selenium2Library* reserves colon to be
    ...              used as a separator in the desired capabilities string.
    ${SUITE_INFO} =  Replace string  ${SUITE_NAME}  :  ${EMPTY}
    ${TEST_INFO} =  Replace string  ${TEST_NAME}  :  ${EMPTY}
    ${BUILD_INFO} =  Set variable
    ...              build:${BUILD_NUMBER},name:${SUITE_INFO} | ${TEST_INFO}
    ${SAUCE_EXTRAS} =  Set variable
    ...                selenium-version:${SELENIUM_VERSION},${BUILD_INFO}
    ${SAUCE_CAPABILITIES} =  Replace String Using Regexp
    ...                      ${DESIRED_CAPABILITIES},${SAUCE_EXTRAS}
    ...                      ^,  ${EMPTY}
    Open browser  ${PLONE_URL}  ${BROWSER}
    ...           remote_url=${REMOTE_URL}
    ...           desired_capabilities=${SAUCE_CAPABILITIES}
    Run keyword and ignore error  Set session id

Set session id
    Keyword should exist  Get session id
    ${SESSION_ID} =  Get session id
    Set test variable  ${SESSION_ID}  ${SESSION_ID}

Report test status
    [Documentation]  Report test status back to SauceLabs. The final test name
    ...              is sent to fix test names missing colons (:).
    Run keyword unless  '${SESSION_ID}' == ''
    ...    Report sauce status  ${SESSION_ID}  ${SUITE_NAME} | ${TEST_NAME}
    ...                         ${TEST_STATUS}  ${TEST_TAGS}  ${REMOTE_URL}
