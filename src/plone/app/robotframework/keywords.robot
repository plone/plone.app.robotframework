*** Settings ***

Documentation  *WARNING* This resource is not stable yet and keywords may be
...            renamed, removed or relocated without notice.

Resource  selenium.robot


*** Keywords ***

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
    Page should contain button  Log in
    Input text for sure  __ac_name  ${userid}
    Input text for sure  __ac_password  ${password}
    Click Button  Log in

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
    Page should contain  logged out


# ----------------------------------------------------------------------------
# Overlays
# ----------------------------------------------------------------------------

Click Overlay Link
    [Arguments]  ${element}
    Click Link  ${element}
    Page Should Contain Element  css=.pb-ajax > div
    Element Should Be Visible  css=.pb-ajax > div

Click Overlay Button
    [Arguments]  ${element}
    Click Button  ${element}
    Page Should Contain Element  css=.pb-ajax > div
    Element Should Be Visible  css=.pb-ajax > div

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
    Page Should Contain Element  id=edit-bar  Edit bar is not available : edit permission missing ?
    Element Should Contain  css=div#edit-bar ul#content-views  ${name}
    Click Link  ${name}

Click Action by id
    [arguments]  ${name}

    Open Action Menu
    Element Should be visible  css=dl#plone-contentmenu-actions dd.actionMenuContent  #${name}
    Click Link  id=${name}

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

    Open Add New Menu
    Click Link  link=Page
    Wait Until Page Contains Element  title
    Input Text  title  ${title}
    Click button  name=form.button.save
    Page Should Contain  Changes saved.

Add folder
    [arguments]  ${title}

    Open Add New Menu
    Click Link  css=#plone-contentmenu-factories a#folder
    Wait Until Page Contains Element  css=#archetypes-fieldname-title input
    Input Text  title  ${title}
    Click Button  Save
    Page should contain  ${title}
    Element should contain  css=#parent-fieldname-title  ${title}

Add document
    [arguments]  ${title}
    Go to  ${PLONE_URL}
    Open add new menu
    Click link  id=document
    Wait Until Page Contains Element  css=#archetypes-fieldname-title input
    Input Text  title  ${title}
    Click Button  Save
    Page should contain  ${title}
    Element should contain  css=#parent-fieldname-title  ${title}

Add news item
    [Arguments]  ${title}
    Go to  ${PLONE_URL}/createObject?type_name=News+Item
    Wait Until Page Contains Element  title
    Input text  title  ${title}
    Click Button  Save


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

    Go to  ${PLONE_URL}/${id}
    Page Should Contain Element  css=body.section-${id}
    Click Rename Action
    Wait Until Page Contains Element  css=input#${id}_id
    Input Text  css=input#${id}_title  ${new_title}
    Click Button  Rename All


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
