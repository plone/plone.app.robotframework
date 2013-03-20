*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/saucelabs.robot

Library  Remote  ${PLONE_URL}/RobotRemoteLibrary

Test Setup  Run keywords  Open SauceLabs test browser  Background
Test Teardown  Run keywords  Report test status  Close all browsers

*** Variables ***

${SELECT_ALL} =   xpath=//*[@id="foldercontents-selectall"]
${CLEAR_SELECTION} =  xpath=//*[@id="foldercontents-clearselection"]
${LISTING_TEMPLATE} =  css=#listing-table .nosort

*** Test cases ***

Test Select All
    Go to homepage
    Click Contents In Edit Bar

    # We have 4 pages on Plone site's root
    Page Should Contain Element  ${SELECT_ALL}
    Click Element  ${SELECT_ALL}
    Page Should Contain Element  ${LISTING_TEMPLATE}  All 4 items in this folder are selected.
    Page Should Contain Element  ${CLEAR_SELECTION}
    Click Element  ${CLEAR_SELECTION}
    Page Should Contain Element  ${SELECT_ALL}

Copy Paste Element
    Go to homepage
    Click Contents In Edit Bar

    Select Checkbox  css=#cb_test1
    Click Button  Copy
    Page Should Contain  1 item(s) copied.
    Click Button  Paste
    Page Should Contain Element  css=#folder-contents-item-copy_of_test1

Cut Paste Element
    Go to homepage
    Click Contents In Edit Bar

    Select Checkbox  css=#cb_test1
    Click Button  Cut
    Page Should Contain  1 item(s) cut.
    Click Button  Paste
    Page Should Contain Element  css=#folder-contents-item-test1

Test Rename Element
    Go to homepage
    Click Contents In Edit Bar

    Select Checkbox  css=#cb_test1
    Click Button  Rename
    Input Text  css=#test1_title  TEST1
    Click Button  Rename All
    Page Should Contain  TEST1

Delete Element
    Go to homepage
    Duplicate Element  test1
    Select Checkbox  css=#cb_copy_of_test1
    Click Button  Delete
    Page Should Contain  Item(s) deleted.
    Page Should Not Contain Element  css=#folder-contents-item-copy_of_test1

*** Keywords ***

Background
    Enable autologin as  Site Administrator
    Go to homepage
    Create Pages

Create Pages
    Go to homepage
    Add Page  test1
    Go to homepage
    Add Page  test2
    Go to homepage
    Add Page  test3
    Go to homepage
    Add Page  test4
    Go to homepage

Remove Pages
    Remove Content  test1
    Remove Content  test2
    Remove Content  test3
    Remove Content  test4

Reorder Element
    [arguments]  ${element}  ${destination}

    Mouse Down  css=#${element} td.draggable
    Mouse Move  css=#${destination} td.draggable
    Mouse Up  css=#${element} td.draggable
    Mouse Out  css=#${element} td.draggable

Duplicate Element
    [arguments]  ${element}
    Click Contents In Edit Bar
    Select Checkbox  css=#cb_${element}
    Click Button  Copy
    Click Button  Paste
