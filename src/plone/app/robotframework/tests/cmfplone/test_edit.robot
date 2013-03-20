*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/saucelabs.robot

Library  Remote  ${PLONE_URL}/RobotRemoteLibrary

Test Setup  Run keywords  Open SauceLabs test browser  Background
Test Teardown  Run keywords  Report test status  Close all browsers

*** Keywords ***

Background
    Enable autologin as  Contributor  Editor
    Go to homepage

*** Test cases ***

Create Folder
    [Tags]  edit
    Add folder  Create folder

Create Document
    [Tags]  edit
    Add document  Create document

Edit document view
    [Tags]  edit  current
    Add document  Edit document view
    Element should be visible  css=li#contentview-edit a
    Click Link  css=li#contentview-edit a
    Element Should Be Visible  css=input#title
    Element Should Be Visible  css=fieldset#fieldset-default
    Element Should Not Be Visible  css=textarea#subject_keywords
    Element Should Not Be Visible  css=fieldset#fieldset-dates
    Element Should Not Be Visible  css=fieldset#fieldset-categorization

Select categorization tab
    [Tags]  edit  current
    Enable autologin as  Site Administrator
    Add document  Select categorization tab
    Element should be visible  css=li#contentview-edit a
    Click Link  css=li#contentview-edit a
    Element should be visible  css=a#fieldsetlegend-categorization
    Click link  css=a#fieldsetlegend-categorization
    Element Should Not Be Visible  css=fieldset#fieldset-default
    Element Should Be Visible  css=textarea#subject_keywords
    Element Should Not Be Visible  css=fieldset#fieldset-dates
    Element Should Be Visible  css=fieldset#fieldset-categorization

Select settings tab
    [Tags]  edit  current
    Add document  Select settings tab
    Element should be visible  css=li#contentview-edit a
    Click Link  css=li#contentview-edit a
    Element should be visible  css=a#fieldsetlegend-settings
    Click link  css=a#fieldsetlegend-settings
    Element Should Not Be Visible  css=fieldset#fieldset-default
    Element Should Not Be Visible  css=textarea#subject_keywords
    Element Should Not Be Visible  css=fieldset#fieldset-dates
    Element Should Be Visible  css=fieldset#fieldset-settings
