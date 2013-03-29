*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/saucelabs.robot

Test Setup  Open SauceLabs test browser
Test Teardown  Run keywords  Report test status  Close all browsers

*** Test cases ***

Test valid login
    Given the overlay login form
     When I enter valid credentials
     Then I am logged in

Test invalid login
    Given the overlay login form
     When I enter invalid credentials
     Then I am not logged in

Test valid login with login keyword
    When I log in with '${TEST_USER_NAME}' and '${TEST_USER_PASSWORD}'
    Then I am logged in

Test invalid login with login keyword
    When I log in with '${TEST_USER_NAME}' and 'invalid'
    Then I am not logged in

*** Keywords ***

the overlay login form
    Click Overlay Link  Log in
    Page should contain element  __ac_name
    Page should contain element  __ac_password
    Page should contain button  Log in

I enter valid credentials
    Input text for sure  __ac_name  ${TEST_USER_NAME}
    Input text for sure  __ac_password  ${TEST_USER_PASSWORD}
    Click Button  Log in

I enter invalid credentials
    Input text for sure  __ac_name  ${TEST_USER_NAME}
    Input text for sure  __ac_password  invalid
    Click Button  Log in

I am logged in
    # FIXME: The following has failed a few times randomly:
    Wait until page contains  ${TEST_USER_ID}

I am not logged in
    Wait until page contains  Login failed

I log in with '${userid}' and '${password}'
    Log in  ${userid}  ${password}
