*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/saucelabs.robot

Suite Setup  Setup Selenium library

Test Setup  Run keywords  Open SauceLabs test browser  Setup
Test Teardown  Run keywords  Report test status  Close all browsers

*** Test cases ***

Content Menu
#   [Tags]  action-menu
    Click Link  An actionsmenu page
    Element Should Not Be Visible  css=a#plone-contentmenu-actions-delete
    Click Link  css=dl#plone-contentmenu-actions dt.actionMenuHeader a
    Element Should Be Visible  css=a#plone-contentmenu-actions-delete
    Click Link  css=dl#plone-contentmenu-actions dt.actionMenuHeader a
    Element Should Not Be Visible  css=a#plone-contentmenu-actions-delete

Switching Actions Menu
#    [Tags]  action-menu
    Click Link  An actionsmenu page
    Element Should Not Be Visible  css=a#plone-contentmenu-actions-delete
    Element Should Not Be Visible  css=a#advanced
    Click Link  css=dl#plone-contentmenu-actions dt.actionMenuHeader a
    Element Should Be Visible  css=a#plone-contentmenu-actions-delete
    Element Should Not Be Visible  css=a#advanced
    Mouse Over  css=dl#plone-contentmenu-actions dt.actionMenuHeader a
    Element Should Be Visible  css=a#plone-contentmenu-actions-delete
    Element Should Not Be Visible  css=a#advanced
    Click Link  css=dl#plone-contentmenu-actions dt.actionMenuHeader a
    Element Should Not Be Visible  css=a#plone-contentmenu-actions-delete
    Element Should Not Be Visible  css=a#advanced

Clicking outside of Actions Menu hides Action Menu
#    [Tags]  action-menu
    Click Link  An actionsmenu page
    Element Should Not Be Visible  css=a#plone-contentmenu-actions-delete
    Element Should Not Be Visible  css=a#advanced
    Click Link  css=dl#plone-contentmenu-actions dt.actionMenuHeader a
    Element Should Be Visible  css=a#plone-contentmenu-actions-delete
    Element Should Not Be Visible  css=a#advanced
    Mouse Down  css=h1
    Wait until keyword succeeds  10s  1s  Element Should Not Be Visible  css=a#plone-contentmenu-actions-delete
    Element Should Not Be Visible  css=a#advanced

Copy Document to Folder Two Different Ways
    Click Link  An actionsmenu page
    Click Action by id  plone-contentmenu-actions-copy
    Wait until keyword succeeds  10s  1s  Page Should Contain  An actionsmenu page copied.
    Click Link  An actionsmenu folder
    Click Action by id  plone-contentmenu-actions-paste
    Wait until keyword succeeds  10s  1s  Page Should Contain  Item(s) pasted.
    # TODO: Exercising the Folder buttons (copy, Cut, Rename, ... ) should be in separate suite
    Click Link  Contents
    Xpath Should Match X Times  //table[@id = 'listing-table']/tbody/tr  1
    Click Button  Paste
    Xpath Should Match X Times  //table[@id = 'listing-table']/tbody/tr  2

Delete Page
    Click Link  An actionsmenu page
    Click Action by id  plone-contentmenu-actions-delete
    Wait until keyword succeeds  10s  1s  Click Button  Delete
    Wait until keyword succeeds  10s  1s  Page Should Not Contain  An actionsmenu page

Rename Page
    Click Link  An actionsmenu page
    Click Action by id  plone-contentmenu-actions-rename
    Wait until keyword succeeds  10s  1s  Input text  new_ids:list  I_AM_RENAMED
    Wait until keyword succeeds  10s  1s  Click Button  Rename All
    Wait until keyword succeeds  10s  1s  Page Should Contain  I_AM_RENAMED

Cut Document and Paste to Folder
    Click Link  An actionsmenu page
    Click Action by id  plone-contentmenu-actions-cut
    Wait until keyword succeeds  10s  1s  Page Should Contain  An actionsmenu page cut.
    Click Link  An actionsmenu folder
    Click Action by id  plone-contentmenu-actions-paste
    Wait until keyword succeeds  10s  1s  Page Should Contain  Item(s) pasted.
    Click Link  Contents
    Xpath Should Match X Times  //table[@id = 'listing-table']/tbody/tr  1

*** Keywords ***

Setup
    Log in as site owner
    Goto homepage
    Add Page  An actionsmenu page
    Goto homepage
    Add folder  An actionsmenu folder
    Goto homepage
