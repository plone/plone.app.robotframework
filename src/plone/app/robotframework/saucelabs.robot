*** Settings ***

Library  Selenium2Library
Library  plone.app.robotframework.SauceLabsLibrary

*** Variables ***

${BUILD_NUMBER} =  manual
${DESIRED_CAPABILITIES} =  tunnel-identifier:manual
${SESSION_ID} =

*** Keywords ***

Open SauceLabs test browser
    ${BUILD_INFO} =  Set variable
    ...           build:${BUILD_NUMBER},name:${SUITE_NAME} | ${TEST_NAME}
    Open browser  ${PLONE_URL}  ${BROWSER}
    ...           remote_url=${REMOTE_URL}
    ...           desired_capabilities=${DESIRED_CAPABILITIES},${BUILD_INFO}
    Run keyword and ignore error  Set session id

Set session id
    Keyword should exist  Get session id
    ${SESSION_ID} =  Get session id
    Set test variable  ${SESSION_ID}  ${SESSION_ID}

Report test status
    Run keyword unless  '${SESSION_ID}' == ''
    ...    Report sauce status  ${SESSION_ID}  ${TEST_STATUS}  ${TEST_TAGS}
