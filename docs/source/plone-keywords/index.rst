==============================================================================
Plone Keywords
==============================================================================


.. toctree::
   :maxdepth: 1

   content.rst
   browser.rst
   login.rst


Misc
----

Goto homepage::

    Goto homepage
        Go to   ${PLONE_URL}
        Page should contain  Powered by Plone & Python

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
