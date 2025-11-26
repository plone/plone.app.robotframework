# Start a single robot test
#
# Start the server
# WSGI_SERVER_HOST=localhost WSGI_SERVER_PORT=50003 robot-server plone.app.robotframework.testing.PLONE_ROBOT_TESTING
#
# Start the test
# WSGI_SERVER_HOST=localhost WSGI_SERVER_PORT=50003 robot src/plone/app/robotframework/tests/test_autologin_library.robot
#
# or run: ROBOT_BROWSER=headlesschrome zope-testrunner --test-path=src --all -t test_autologin_library.robot
#
*** Settings ***

Resource    plone/app/robotframework/browser.robot

Library    Remote    ${PLONE_URL}/RobotRemote

Test Setup    Run Keywords    Plone test setup
Test Teardown    Run keywords     Plone test teardown

# disable headless mode for browser
# set the variable BROWSER to chrome or firefox
# *** Variables ***
# ${BROWSER}    chrome

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
    Enable autologin as    ${ROLE}
    Go to    ${PLONE_URL}

I open the personal menu
    Click    //a[@id="personaltools-menulink"]

I see the Site Setup -link
    Wait For Elements State    //a[@id="personaltools-plone_setup"]    visible

I cannot see the Site Setup -link
    Wait For Elements State    //a[@id="personaltools-plone_setup"]    hidden

I go to the front page
    Go to  ${PLONE_URL}

I can add a new folder
    Add folder  New folder
    Go to  ${PLONE_URL}/new-folder
    Get Element count    :text("New folder"):visible    >    0

I've created a test folder
    Enable autologin as    Contributor
    Set autologin username    Authenticated
    Go to    ${PLONE_URL}
    Add folder    Test folder
    Go to    ${PLONE_URL}/test-folder
    Get Element count    :text("Test folder"):visible    >    0

I'm logged in as an 'Authenticated'
    Enable autologin as  Authenticated

I'm logged in again as an 'Authenticated'
    Enable autologin as  Authenticated

I go to my test folder
    Go to  ${PLONE_URL}/test-folder

I can add a sub-folder
    Add folder  Sub folder
    Go to  ${PLONE_URL}/test-folder/sub-folder
    Get Element count    :text("Sub folder"):visible    >    0

Someone else has created a test folder
    Enable autologin as  Contributor
    Go to  ${PLONE_URL}
    Add folder  Test folder

I go to the test folder
    Go to  ${PLONE_URL}/test-folder

I get insufficient privileges error
    Get Element count    :text("Insufficient Privileges"):visible    >    0

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
    Get Element count    :text("Insufficient Privileges"):visible    >    0

Add folder
    [arguments]    ${title}
    ${result} =  Add content    folder    ${title}
    RETURN    ${result}


Add document
    [arguments]    ${title}
    Go to    ${PLONE_URL}
    ${result} =  Add Page    ${title}
    RETURN    ${result}

Add Page
    [arguments]    ${title}
    ${result} =  Add content    document    ${title}
    RETURN    ${result}

Add content
    # DEXTERITY content only
    [arguments]    ${content_type}    ${title}
    Open add new menu
    Click    //a[@id="${content_type}"]
    Type Text    //input[@name="form.widgets.IDublinCore.title"]    ${title}
    Click    //button[@name="form.buttons.save"]
    Get Element count    :text("Item created"):visible    >    0
    Get Element count    :text("${title}"):visible    >    0
    Displayed content title should be    ${title}
    ${location} =  Get Url
    RETURN    ${location}

Open Add New Menu
    Open Menu    plone-contentmenu-factories


Open Menu
    [Arguments]    ${elementId}

    Click    //*[@id="${elementId}"]
    Wait For Elements State    //*[@id="${elementId}"]/ul    visible    timeout=2 s


Displayed content title should be
    [arguments]    ${title}
    Get Element count    xpath=//header/h1[contains(., "${title}")]    >    0
