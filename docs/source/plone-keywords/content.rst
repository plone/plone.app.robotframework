==============================================================================
Plone Content Keywords
==============================================================================

Robot Framework / Selenium2Library keywords to create/delete/change Plone
content.

- Use a test-folder (like in p.a.testing) for isolation and to avoid problems
  for instance with name clashes in the global navigation.

- We currently have two different ways to create content:

  - Create <portal_type> <title>: create content object in portal root / test
    folder.

  - Add <portal_type> <title>: add content object in current context / folder.

  Maybe we can come up with a smart way to do both with one keyword with
  optional parameters?


Create content
==============

Create folder (Create a folder object within the test-folder)::

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

Create page (Create a page object within the test-folder)::

    Create page
        [arguments]  ${title}

        Create folder  Folder for ${title}
        Open Add New Menu
        Click Link  css=#plone-contentmenu-factories a#document
        Element should be visible  css=#archetypes-fieldname-title input
        Input Text  title  ${title}
        Click Button  Save
        Page should contain  ${title}
        Element should contain  css=#parent-fieldname-title  ${title}


Add content
===========

Add page (Add a page object in the current context/location)::

    Add page
        [arguments]  ${title}

        Open Add New Menu
        Click Link  link=Page
        Input Text  title  ${title}
        Click button  name=form.button.save
        Page Should Contain  Changes saved.
