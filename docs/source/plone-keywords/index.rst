==============================================================================
Plone Keywords
==============================================================================


.. toctree::
   :maxdepth: 1

   content.rst
   browser.rst
   login.rst
   editbar.rst


Misc
----

Goto homepage::

    Goto homepage
        Go to   ${PLONE_URL}
        Page should contain  Powered by Plone & Python

Click Overlay Link::

    Click Overlay Link
        [Arguments]  ${element}
        Click Link  ${element}
        Wait Until Page Contains Element  css=div.pb-ajax div#content-core

Should be above::

    Should be above
        [Arguments]  ${locator1}  ${locator2}

        ${locator1-position} =  Get vertical position  ${locator1}
        ${locator2-position} =  Get vertical position  ${locator2}
        Should be true  ${locator1-position} < ${locator2-position}

Remove Content::

    Remove Content
        [arguments]  ${id}

        Go to  ${PLONE_URL}/${id}
        Page Should Contain Element  css=body.section-${id}
        Click Delete Action
        Wait Until Page Contains Element  css=input.destructive
        Click Button  css=input.destructive
        Page Should Contain  Plone site

Rename Content Title::

    Rename Content Title
        [arguments]  ${id}  ${new_title}

        Go to  ${PLONE_URL}/${id}
        Page Should Contain Element  css=body.section-${id}
        Click Rename Action
        Wait Until Page Contains Element  css=input#${id}_id
        Input Text  css=input#${id}_title  ${new_title}
        Click Button  Rename All
