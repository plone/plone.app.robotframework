Plone Keywords
==============


Start browser and wake plone up
    [Arguments]  ${ZOPE_LAYER_DOTTED_NAME}

    Start Zope Server  ${ZOPE_LAYER_DOTTED_NAME}
    Zodb setup
    Set Selenium timeout  15s
    Set Selenium implicit wait  1s

    ${previous}  Register keyword to run on failure  Close Browser
    Wait until keyword succeeds  2min  3s  Access plone
    Register keyword to run on failure  ${previous}


    Wait until keyword succeeds  30s  1s  Log in as site owner
    Log out
    Zodb teardown

Log in as site owner
    ${name} =  Get site owner name
    ${password} =  Get site owner password
    Log in  ${name}  ${password}

Access plone
    Open browser  ${ZOPE_URL}  ${BROWSER}
    Goto homepage
    [Return]  True

Close browser and selenium server
    Close browser
    Stop Zope Server

Goto homepage
    Go to   ${PLONE_URL}
    Page should contain  Powered by Plone & Python

Log out
    Go to  ${PLONE_URL}/logout
    Page should contain  logged out

Log in
    [Arguments]  ${userid}  ${password}
    Go to  ${PLONE_URL}/login_form
    Page should contain element  __ac_name
    Input text  __ac_name  ${userid}
    Input text  __ac_password  ${password}
    Click Button  Log in
    Page should contain element  css=#user-name
    Go to  ${PLONE_URL}
    [Return]  True

Click Overlay Link
    [Arguments]  ${element}
    Click Link  ${element}
    Wait Until Page Contains Element  css=div.pb-ajax div#content-core

Should be above
    [Arguments]  ${locator1}  ${locator2}

    ${locator1-position} =  Get vertical position  ${locator1}
    ${locator2-position} =  Get vertical position  ${locator2}
    Should be true  ${locator1-position} < ${locator2-position}

Open Menu
    [Arguments]  ${elementId}

    Element Should Be Visible  css=dl#${elementId} span
    Element Should Not Be Visible  css=dl#${elementId} dd.actionMenuContent
    Click link  css=dl#${elementId} dt.actionMenuHeader a
    Wait until keyword succeeds  1  5  Element Should Be Visible  css=dl#${elementId} dd.actionMenuContent

Open User Menu
    Open Menu  portal-personaltools

Open Add New Menu
    Open Menu  plone-contentmenu-factories

Open Display Menu
    Open Menu  plone-contentmenu-display

Open Action Menu
    Open Menu  plone-contentmenu-actions

Open Workflow Menu
    Open Menu  plone-contentmenu-workflow

Click ${name} In Edit Bar
    Element Should Contain  css=div#edit-bar ul#content-views  ${name}
    Click Link  ${name}

Click Actions ${name}
    Open Action Menu
    Element Should Contain  css=dl#plone-contentmenu-actions dd.actionMenuContent  ${name}
    Click Link  ${name}

Click Cut Action
    Click Actions Cut

Click Copy Action
    Click Actions Copy

Click Delete Action
    Click Actions Delete

Click Rename Action
    Click Actions Rename

Add Page
    [arguments]  ${title}

    Open Add New Menu
    Click Link  link=Page
    Input Text  title  ${title}
    Click button  name=form.button.save
    Page Should Contain  Changes saved.

Remove Content
    [arguments]  ${id}

    Go to  ${PLONE_URL}/${id}
    Page Should Contain Element  css=body.section-${id}
    Click Delete Action
    Wait Until Page Contains Element  css=input.destructive
    Click Button  css=input.destructive
    Page Should Contain  Plone site

Rename Content Title
    [arguments]  ${id}  ${new_title}

    Go to  ${PLONE_URL}/${id}
    Page Should Contain Element  css=body.section-${id}
    Click Rename Action
    Wait Until Page Contains Element  css=input#${id}_id
    Input Text  css=input#${id}_title  ${new_title}
    Click Button  Rename All


Create folder
    [arguments]  ${title}

    Goto homepage
    Open Add New Menu
    Click Link  css=#plone-contentmenu-factories a#folder
    Element should be visible  css=#archetypes-fieldname-title input
    Input Text  title  ${title}
    Click Button  Save
    Page should contain  ${title}
    Element should contain  css=#parent-fieldname-title  ${title}

Create document
    [arguments]  ${title}

    Create folder  Folder for ${title}
    Open Add New Menu
    Click Link  css=#plone-contentmenu-factories a#document
    Element should be visible  css=#archetypes-fieldname-title input
    Input Text  title  ${title}
    Click Button  Save
    Page should contain  ${title}
    Element should contain  css=#parent-fieldname-title  ${title}

