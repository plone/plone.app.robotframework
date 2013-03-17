*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/saucelabs.robot

Suite Setup  Setup Selenium library

Test Setup  Open SauceLabs test browser
Test Teardown  Run keywords  Report test status  Close all browsers

*** Test cases ***

Test Valid Login
    Given the overlay login form
    When I enter valid credentials
    Then I am logged in

Test Invalid Login
    Given the overlay login form
    When I enter invalid credentials
    Then I am not logged in

*** Keywords ***

the overlay login form
    Click Overlay Link  Log in

I enter valid credentials
    Input text  __ac_name  ${TEST_USER_NAME}
    Input text  __ac_password  ${TEST_USER_PASSWORD}
    Click Button  Log in

I enter invalid credentials
    Input text  __ac_name  ${TEST_USER_NAME}
    Input text  __ac_password  ""
    Click Button  Log in

I am logged in
    Wait until page contains  ${TEST_USER_ID}

I am not logged in
    Wait until page contains  Login failed
