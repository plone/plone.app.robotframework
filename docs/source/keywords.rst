==============================================================================
Selenium2Library Keywords
==============================================================================

.. note::

    TODO: The general idea of this document is to give a first introduction to
    the Selenium2Library keywords. We do NOT want to re-document the existing
    Selenium2Library documentation.

Selenium2Library is a web testing library for Robot Framework. It provides you
with several low-level keywords to access certain elements of a web page, to
conduct actions on a web page and to test if a page met certain acceptance critera.


First Example
=============

TODO: We need a simple first example to explain the basic concepts. Here are
some ideas.


Test Google Search For Plone::

    Test Google Search For Plone
        Go to  www.google.com

        Input text  id=gbqfq  Plone
        Click Button  id=gbqfbb

        Page should contain  Plone CMS: Open Source Content Management
        Page should contain  plone.org

Test Plone Search::

    Test Plone Search
        Go to  http://localhost:55001/plone/

        Input Text  SearchableText  batman
        Click Button  Search

        Page should contain  Search results
        Page should contain  Welcome to Plone

Test Plone Live Search::

    Test Plone Live Search
        Go to  http://localhost:55001/plone/

        Input Text  SearchableText  Plone

        Page should contain  Search results
        Page should contain  Welcome to Plone


Test Plone Contact Form::

    Test Plone Contact Form

        Click Link  Contact
        Page should contain  Contact
        ...


TODO: Explain the concepts of tests

Form:

- Precondition (Given)
- Action (When)
- Postcondition/Test (Then)

These parts should be separated by blank lines.


Preconditions
=============

- Open Browser???
- Go to ...

.. seealso::

    http://rtomac.github.com/robotframework-selenium2library/doc/Selenium2Library.html#Go%20To

Actions
=======

Click on elements
-----------------

- Click Button
- Click Element
- Click Image
- Click Link

.. seealso::

    http://rtomac.github.com/robotframework-selenium2library/doc/Selenium2Library.html#Click%20Button

Fill out form
-------------

- Input Text
- Input Password

.. seealso::

    http://rtomac.github.com/robotframework-selenium2library/doc/Selenium2Library.html#Input%20Text


Postconditions
==============

- Page Should Contain <locator>

- Page Should Contain Button | Checkbox | Element | Image | Link | List | Radio Button | Textfield <locator>

- Page Should Not Contain <locator>

.. seealso::

    http://rtomac.github.com/robotframework-selenium2library/doc/Selenium2Library.html#Page%20Should%20Contain


Locating elements
=================

Locating element by id::


    Click Element  id=submit
    Click Element  name=submit
    Click Element  xpath=//div[@id='my_element']
    Click Element  dom=document.images[56]
    Click Element  link=Save
    Click Element  css=div.submit    Matches by CSS selector
    Click Element  tag=div     Matches by HTML tag name

.. seealso::

    'locating elements' section http://rtomac.github.com/robotframework-selenium2library/doc/Selenium2Library.html
