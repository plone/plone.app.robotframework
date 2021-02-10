*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/saucelabs.robot
Resource  plone/app/robotframework/selenium.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Run keywords  Plone test setup
Test Teardown  Run keywords  Plone test teardown

*** Test Cases ***

Site Administrator can access control panel
    Given I'm logged in as a 'Site Administrator'
     When I open the personal menu
     Then I see the Site Setup -link

Contributor cannot access control panel
    Given I'm logged in as a 'Contributor'
     When I open the personal menu
     Then I cannot see the Site Setup -link

Contributor can create a folder
    Given I'm logged in as a 'Contributor'
     When I go to the front page
     Then I can add a new folder

Owner can add a sub-folder under her own folder
    Given I've created a test folder
      And I'm logged in again as an 'Authenticated'
     When I go to my test folder
     Then I can add a sub-folder

Authenticated cannot add a sub-folder under a folder by someone else
    Given Someone else has created a test folder
      And I'm logged in as an 'Authenticated'
     When I go to the test folder
     Then I get insufficient privileges error

Contributors cannot edit each other's pages
    Given Contributor A has created a new page
     When Contributor B tries to edit that page
     Then she gets insufficient privileges error

*** Keywords ***

I'm logged in as a '${ROLE}'
    Enable autologin as  ${ROLE}
    Go to  ${PLONE_URL}

I open the personal menu
    Click link  css=#portal-personaltools > a

I see the Site Setup -link
    Element should be visible  css=#personaltools-plone_setup

I cannot see the Site Setup -link
    Element should not be visible  css=#personaltools-plone_setup

I go to the front page
    Go to  ${PLONE_URL}

I can add a new folder
    Add folder  New folder
    Go to  ${PLONE_URL}/new-folder
    Page should contain  New folder

I've created a test folder
    Enable autologin as  Contributor
    Set autologin username  Authenticated
    Go to  ${PLONE_URL}
    Add folder  Test folder
    Go to  ${PLONE_URL}/test-folder
    Page should contain  Test folder

I'm logged in as an 'Authenticated'
    Enable autologin as  Authenticated

I'm logged in again as an 'Authenticated'
    Enable autologin as  Authenticated

I go to my test folder
    Go to  ${PLONE_URL}/test-folder

I can add a sub-folder
    Add folder  Sub folder
    Go to  ${PLONE_URL}/test-folder/sub-folder
    Page should contain  Sub folder

Someone else has created a test folder
    Enable autologin as  Contributor
    Go to  ${PLONE_URL}
    Add folder  Test folder

I go to the test folder
    Go to  ${PLONE_URL}/test-folder

I get insufficient privileges error
    Page should contain  Insufficient Privileges

Contributor A has created a new page
    Enable autologin as  Contributor
    Set autologin username   Contributor A
    Go to  ${PLONE_URL}
    Add document  New page

Contributor B tries to edit that page
    Enable autologin as  Contributor
    Set autologin username   Contributor B
    Go to  ${PLONE_URL}/new-page/edit

She gets insufficient privileges error
    Page should contain  Insufficient Privileges
