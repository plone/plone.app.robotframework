*** Comments ***
# Start a single robot test
#
# Start the server
# WSGI_SERVER_HOST=localhost WSGI_SERVER_PORT=50003 robot-server plone.app.robotframework.testing.PLONE_ROBOT_TESTING
#
# Start the test
# WSGI_SERVER_HOST=localhost WSGI_SERVER_PORT=50003 robot src/plone/app/robotframework/tests/test_content_library.robot
#
# or run: ROBOT_BROWSER=headlesschrome zope-testrunner --test-path=src --all -t test_content_library.robot
#


*** Settings ***
Resource            plone/app/robotframework/browser.robot
Library             Remote    ${PLONE_URL}/RobotRemote

Test Setup          Run Keywords    Plone test setup
Test Teardown       Run keywords    Plone test teardown
# disable headless mode for browser
# set the variable BROWSER to chrome or firefox
# *** Variables ***
# ${BROWSER}    chrome


*** Test Cases ***
Test create content
    Enable autologin as    Contributor
    Create content    type=Document    id=example-document    title=Example document
    Go to    ${PLONE_URL}/example-document
    Get Element count    :text("Example document"):visible    >    0

Test create content with custom id
    Enable autologin as    Contributor
    Create content    type=Document    id=example    title=Example document
    Go to    ${PLONE_URL}/example
    Get Element count    :text("Example document"):visible    >    0

Test create content inside a container specified by a uid
    Enable autologin as    Contributor
    ${folder_uid} =    Create content    type=Folder    id=folder    title=Example folder
    Create content    type=Document    id=example    title=Example document    container=${folder_uid}
    Go to    ${PLONE_URL}/folder/example
    Get Element count    :text("Example document"):visible    >    0

Test create content inside a container specified by a path
    Enable autologin as    Contributor
    Create content    type=Folder    id=folder    title=Example folder
    Create content    type=Document    id=example    title=Example document    container=/plone/folder
    Go to    ${PLONE_URL}/folder/example
    Get Element count    :text("Example document"):visible    >    0

Test uid to url resolving
    Enable autologin as    Contributor
    ${uid} =    Create content    type=Document    id=example-document    title=Example document
    ${url} =    UID to URL    ${uid}
    Go to    ${url}
    Get Element count    :text("Example document"):visible    >    0

Test path to uid resolving
    Enable autologin as    Contributor
    ${uid} =    Create content    type=Document    id=example-document    title=Example document
    ${result_uid} =    Path to UID    /plone/example-document
    Should Be Equal    ${uid}    ${result_uid}

Test fire transition
    Enable autologin as    Contributor    Reviewer
    ${uid} =    Create content    type=Document    id=example-document    title=Example document
    Fire transition    ${uid}    publish
    Disable autologin
    Go to    ${PLONE_URL}/example-document
    Get Element count    :text("Example document"):visible    >    0

Test global allow
    Enable autologin as    Contributor
    Global Allow    Document
    ${uid} =    Create content    type=Document    id=example-document    title=Example document
