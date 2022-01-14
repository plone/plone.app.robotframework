*** Settings ***

Documentation  *WARNING* This resource is not stable yet and keywords may be
...            renamed, removed or relocated without notice.

Resource  selenium.robot
Resource  user.robot

*** Keywords ***

Debug
    [Documentation]  Pause test execution for test debugging purposes.
    ...
    ...              When DebugLibrary is found, pauses test execution
    ...              with interactive robotframework debugger (REPL)
    ...              in the current shell. This s based on
    ...              ``robotframework-debuglibrary`` and requires that the
    ...              used Python is compiled with ``readline``-support.
    ...
    ...              When DebugLibrary is NOT found, pauses test execution
    ...              with Dialogs-library's Pause Execution library, which
    ...              requires that the used Python is compiled with TkInter
    ...              support.
    ...
    ...              When Dialogs-library cannot be imported, pauses test
    ...              execution with interactive Python debugger (REPL)
    ...              in the current shell.
    ${debug} =  Run keyword and ignore error
    ...          Import library  DebugLibrary  WITH NAME  DebugLibrary
    ${dialogs} =  Run keyword and ignore error
    ...           Import library  Dialogs  WITH NAME  DialogsLibrary
    ${fallback} =  Run keyword and ignore error
    ...            Import library  plone.app.robotframework.keywords.Debugging
    ...            WITH NAME  DebuggingLibrary
    Run keyword if  '${debug}[0]' == 'PASS'
    ...             DebugLibrary.Debug
    Run keyword if  '${debug}[0]' == 'FAIL' and '${dialogs}[0]' == 'PASS'
    ...             DialogsLibrary.Pause Execution
    Run keyword if  '${debug}[0]' == 'FAIL' and '${dialogs}[0]' == 'FAIL'
    ...             DebuggingLibrary.Stop

Pause
    [Documentation]  Visually pause test execution with interactive dialog by
    ...              importing **Dialogs**-library and calling its
    ...              **Pause Execution**-keyword.
    Import library  Dialogs
    Pause execution

# ----------------------------------------------------------------------------
# Access Resources
# ----------------------------------------------------------------------------

Go to homepage
    Go to   ${PLONE_URL}
    Wait until location is  ${PLONE_URL}

# ----------------------------------------------------------------------------
# Login/Logout
# ----------------------------------------------------------------------------

Log in
    [Documentation]  Log in to the site as ${userid} using ${password}. There
    ...              is no guarantee of where in the site you are once this is
    ...              done. (You are responsible for knowing where you are and
    ...              where you want to be)
    [Arguments]  ${userid}  ${password}
    Go to  ${PLONE_URL}/login_form
    Page should contain element  __ac_name
    Page should contain element  __ac_password
    Page should contain element  ${BUTTON_LOGIN_SELECTOR}
    Input text for sure  __ac_name  ${userid}
    Input text for sure  __ac_password  ${password}
    Click Element  ${BUTTON_LOGIN_SELECTOR}

Log in as test user

    Log in  ${TEST_USER_NAME}  ${TEST_USER_PASSWORD}

Log in as site owner
    [Documentation]  Log in as the SITE_OWNER provided by plone.app.testing,
    ...              with all the rights and privileges of that user.
    Log in  ${SITE_OWNER_NAME}  ${SITE_OWNER_PASSWORD}

Log in as test user with role
    [Arguments]  ${usrid}  ${role}

    # We need a generic way to login with a user that has one or more roles.

    # Do we need to be able to assign multiple roles at once?

    # Do we need to assign roles to arbitray users or is it sufficient if we
    # always assign those roles to the test user?

Log out
    Go to  ${PLONE_URL}/logout
    Page Should Contain Element  css=#login-form


# ----------------------------------------------------------------------------
# Overlays
# ----------------------------------------------------------------------------

Click Overlay Link
    [Arguments]  ${element}
    Click Link  ${element}
    Wait until keyword succeeds  10  1  Page Should Contain Element  css=.pb-ajax > div,.modal
    Element Should Be Visible  css=.pb-ajax > div,.modal

Click Overlay Button
    [Arguments]  ${element}
    Click Button  ${element}
    Wait until page contains element  css=.pb-ajax > div,.modal
    Page Should Contain Element  css=.pb-ajax > div,.modal
    Element Should Be Visible  css=.pb-ajax > div,.modal

Should be above
    [Arguments]  ${locator1}  ${locator2}

    ${locator1-position} =  Get vertical position  ${locator1}
    ${locator2-position} =  Get vertical position  ${locator2}
    Should be true  ${locator1-position} < ${locator2-position}


# ----------------------------------------------------------------------------
# Menu / Edit Bar
# ----------------------------------------------------------------------------

Open Menu
    [Arguments]  ${elementId}

    Element Should Be Visible  css=#${elementId} span
    Element Should Not Be Visible  css=#${elementId} > div > ul
    Click link  css=#${elementId} a
    Wait Until Element Is Visible  css=#${elementId} > div > ul

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
    Page Should Contain Element  id=edit-bar  Edit bar is not available : edit permission missing ?
    Element Should Contain  css=div#edit-bar ul#content-views  ${name}
    Click Link  ${name}

Click Action by id
    [arguments]  ${name}

    Open Action Menu
    Click Link  id=plone-contentmenu-actions-${name}

Click Cut Action
    Click Action by id  cut

Click Copy Action
    Click Action by id  copy

Click Delete Action
    Click Action by id  delete

Click Rename Action
    Click Action by id  rename


# ----------------------------------------------------------------------------
# Workflow
# ----------------------------------------------------------------------------

Publish Object
    [Documentation]  *DEPRECATED* Use keyword `Workflow Publish` instead.

    Workflow Publish

# XXX: Check Status Message could be moved to a different section

Check Status Message
    [Arguments]  ${message}

    Page Should Contain Element  css=dl.portalMessage dt  Info
    Page Should Contain Element  css=dl.portalMessage dd  ${message}

Trigger Workflow Transition
    [Arguments]  ${transitionId}

    Open Workflow Menu
    Click Link  workflow-transition-${transitionId}
    Check Status Message  Item state changed.

Workflow Submit
    Trigger Workflow Transition  submit

Workflow Retract
    Trigger Workflow Transition  retract

Workflow Reject
    Trigger Workflow Transition  reject

Workflow Publish
    Trigger Workflow Transition  publish

Workflow Make Private
    Trigger Workflow Transition  hide

Workflow Promote to Draft
    Trigger Workflow Transition  show


# ----------------------------------------------------------------------------
# Create Content
# ----------------------------------------------------------------------------

Add Page
    [arguments]  ${title}
    ${result} =  Add content  document  ${title}
    [return]  ${result}

Add folder
    [arguments]  ${title}
    ${result} =  Add content  folder  ${title}
    [return]  ${result}

Add document
    [arguments]  ${title}
    Go to  ${PLONE_URL}
    ${result} =  Add Page  ${title}
    [return]  ${result}

Add news item
    [arguments]  ${title}
    ${result} =  Add content  news-item  ${title}
    [return]  ${result}

Displayed content title should be
    [arguments]  ${title}
    Page should contain element  xpath=//header/h1[contains(., "${title}")]

Add content
    # DEXTERITY content only
    [arguments]  ${content_type}  ${title}
    Open add new menu
    Click Link  ${content_type}
    Wait until page contains element  css=#form-widgets-IDublinCore-title
    Input Text  form.widgets.IDublinCore.title  ${title}
    Wait until page contains element  ${BUTTON_SAVE_SELECTOR}
    Click button  ${BUTTON_SAVE_SELECTOR}
    Wait until page contains  Item created
    Page should contain  ${title}
    Displayed content title should be  ${title}
    ${location} =  Get Location
    [return]  ${location}


# ----------------------------------------------------------------------------
# Content Actions
# ----------------------------------------------------------------------------

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

    Go to  ${PLONE_URL}/${id}/object_rename
    Input Text for sure  css=input#${id}_title  ${new_title}
    Click Button  Rename All
    Go to  ${PLONE_URL}/${id}


# ----------------------------------------------------------------------------
# Content Management Views
# ----------------------------------------------------------------------------

Open history popup
    Click Overlay Link  History


# ----------------------------------------------------------------------------
# Content Management Views
# ----------------------------------------------------------------------------

Open wizard tab
    [arguments]  ${title}
    Click link  link=${title}


# ----------------------------------------------------------------------------
# Widgets
# ----------------------------------------------------------------------------

Set Reference Browser Field Value
    [arguments]  ${fieldName}  @{path}
    Click Overlay Button  css=#archetypes-fieldname-${fieldName} input[type=button]
    ${len}=  Get Length  ${path}
    :FOR  ${i}  IN RANGE  ${len}
    \   Run Keyword If  ${i}!=${len}-1  Click Link  xpath=//table[contains(@class, 'group')]//a[contains(., "@{path}[${i}]")]
    \   Run Keyword If  ${i}==${len}-1  Checkbox Select  @{path}[${i}]

Checkbox Select
    [arguments]  ${title}
    ${for}=  Get Element Attribute  xpath=//table[contains(@class, 'group')]//label[contains(., "${title}")]@for
    Select Checkbox  id=${for}

Remove line from textarea
    [arguments]  ${fieldName}  ${value}
    ${lines}=  Get value  name=${fieldName}
    ${lines}=  Remove String  ${lines}  ${value}\n
    Input Text  name=${fieldName}  ${lines}
