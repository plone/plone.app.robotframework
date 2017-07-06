==============================================================================
Plone Keywords
==============================================================================

plone.act provides high-level keywords to test Plone. Idealy it should provide
all the keywords that are necessary to write acceptance test in Plone.


.. toctree::
   :maxdepth: 1

   content.rst
   generic.rst
   browser.rst
   login.rst
   history.rst
   edit-wizard-tabs.rst
   reference-browser-widget.rst


Using plone.app.testing variables
---------------------------------

You can use existing plone.app.testing variables defined in `plone/app/testing/interfaces.py <https://github.com/plone/plone.app.testing/blob/master/plone/app/testing/interfaces.py>`_. in your acceptance tests::

    *** Settings ***

    Library  plone.act.PloneLibrary
    Library  Selenium2Library  run_on_failure=Capture Page Screenshot
    Variables  plone/app/testing/interfaces.py


    *** Test cases ***

    Test variable file
        Should Be Equal  ${PLONE_SITE_ID}     plone
        Should Be Equal  ${PLONE_SITE_TITLE}  Plone site
        Should Be Equal  ${DEFAULT_LANGUAGE}  en

        Should Be Equal  ${TEST_USER_NAME}  test-user
        Should Be Equal  ${TEST_USER_ID}    test_user_1_
        Should Be Equal  ${TEST_USER_PASSWORD}  secret
        #Should Be Equal  ${TEST_USER_ROLES}  ['Member',]

        Should Be Equal  ${SITE_OWNER_NAME}      admin
        Should Be Equal  ${SITE_OWNER_PASSWORD}  secret


Misc
----

Goto homepage::

    Goto homepage
        Go to   ${PLONE_URL}
        Page should contain  Powered by Plone & Python

..note::

    I think we should deprecate that keyword because it is too close to the
    existing "Go to" selenium2library keyword.


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
