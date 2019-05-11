*** Settings ***

Resource  plone/app/robotframework/saucelabs.robot
Resource  plone/app/robotframework/selenium.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Run keywords  Plone test setup
Test Teardown  Run keywords  Plone test teardown

*** Test Cases ***

Test create content
    Enable autologin as  Contributor
    Create content  type=Document  id=example-document  title=Example document
    Go to  ${PLONE_URL}/example-document
    Page should contain  Example document

Test create content with custom id
    Enable autologin as  Contributor
    Create content  type=Document  id=example  title=Example document
    Go to  ${PLONE_URL}/example
    Page should contain  Example document

Test create content inside a container specified by a uid
    Enable autologin as  Contributor
    ${folder_uid}  Create content  type=Folder  id=folder  title=Example folder
    Create content  type=Document  id=example  title=Example document  container=${folder_uid}
    Go to  ${PLONE_URL}/folder/example
    Page should contain  Example document

Test create content inside a container specified by a path
    Enable autologin as  Contributor
    Create content  type=Folder  id=folder  title=Example folder
    Create content  type=Document  id=example  title=Example document  container=/plone/folder
    Go to  ${PLONE_URL}/folder/example
    Page should contain  Example document

Test uid to url resolving
    Enable autologin as  Contributor
    ${uid} =  Create content  type=Document  id=example-document
    ...  title=Example document
    ${url} =  UID to URL  ${uid}
    Go to  ${url}
    Page should contain  Example document

Test path to uid resolving
    Enable autologin as  Contributor
    ${uid} =  Create content  type=Document  id=example-document
    ...  title=Example document
    ${result_uid} =  Path to UID  /plone/example-document
    Should Be Equal  ${uid}  ${result_uid}

Test fire transition
    Enable autologin as  Contributor  Reviewer
    ${uid} =  Create content  type=Document  id=example-document
    ...  title=Example document
    Fire transition  ${uid}  publish
    Disable autologin
    Go to  ${PLONE_URL}/example-document
    Page should contain  Example document

Test global allow
    Enable autologin as  Contributor
    Global Allow  Document
    ${uid} =  Create content  type=Document  id=example-document
    ...  title=Example document
