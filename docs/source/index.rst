Writing Robot Framework tests for Plone
=======================================

`plone.app.robotframework`_ provides `Robot Framework`_-compatible tools and
resources for writing functional Selenium_-tests (including acceptance tests)
for `Plone CMS`_ and its add-ons.

This documentation gives you everything to get started in writing and
executing functional Selenium tests (including acceptance tests) for Plone or
your own Plone add-on. We depend  on two testing frameworks, `Robot Framework`_
and Selenium_ (with Selenium2Library_), and our tools and resources provided
in *plone.app.robotframework*.

`Robot Framework`_ is a generic test automation framework for acceptance
testing and acceptance test-driven development (ATDD), even for behavior driven
development (BDD). It has easy-to-use plain text test syntax and utilizes the
keyword-driven testing approach. Selenium is a web browser automation framework
that exercises the browser as if the user was interacting with the browser.

.. _plone.app.robotframework: http://pypi.python.org/pypi/plone.app.robotframework
.. _Robot Framework: http://robotframework.org/
.. _Plone CMS: http://plone.org/
.. _Selenium: http://seleniumhq.org/
.. _Selenium2Library: https://pypi.python.org/pypi/robotframework-selenium2library


Start here
----------

Start here to learn the default way of writing Robot Framework tests to be
run just next to your other Plone-tests with `zope.testrunner`_:

.. toctree::
   :maxdepth: 2

   happy

.. _zope.testrunner: http://pypi.python.org/pypi/zope.testrunner


Print these
-----------

Print these keyword libraries to be easily available when writing Robot
Framework tests, because they provide the basic building blocks for your
tests:

* `Robot Framework built-in library documentation`__
* `Robot Framework Selenium2Library documentation`__

__ http://robotframework.googlecode.com/hg/doc/libraries/BuiltIn.html?r=2.8.1
__ http://rtomac.github.com/robotframework-selenium2library/doc/Selenium2Library.html


Advanced topics
---------------

.. toctree::
   :maxdepth: 1
   :titlesonly:

   travis-ci
   saucelabs
   robot
   debugging
   reload
   ride


User keywords
-------------

- :download:`libdoc/user_keywords.html`
- :download:`libdoc/user_saucelabs.html`
- :download:`libdoc/user_selenium.html`
- :download:`libdoc/user_server.html`


Remote keywords
---------------

- :download:`libdoc/remote_autologin.html`
- :download:`libdoc/remote_content.html`
- :download:`libdoc/remote_genericsetup.html`
- :download:`libdoc/remote_i18n.html`
- :download:`libdoc/remote_mockmailhost.html`
- :download:`libdoc/remote_quickinstaller.html`
- :download:`libdoc/remote_users.html`
- :download:`libdoc/remote_zope2server.html`


Python keywords
---------------

- :download:`libdoc/python_debugging.html`
- :download:`libdoc/python_layoutmath.html`
- :download:`libdoc/python_saucelabs.html`
- :download:`libdoc/python_zope2server.html`


Other resources
---------------

* `How to write good Robot Framework test cases`__
* `List of available Robot Framework test libraries`__
* :doc:`plone.app.robotframework examples of use <examples>`

__ http://code.google.com/p/robotframework/wiki/HowToWriteGoodTestCases
__ http://code.google.com/p/robotframework/wiki/TestLibraries


Old tutorials
-------------

.. toctree::
   :maxdepth: 1
   :titlesonly:

   Write a robot test for a new Plone add-on <templer>
   Write a robot test for an existing Plone add-on <tutorial>
   Speed up your test writing with robot-server <server>
   Speed up your BDD Given-clauses with a remote library <remote>


.. toctree::
   :hidden:

   examples
   keywords
   plone-keywords/browser
   plone-keywords/content
   plone-keywords/edit-wizard-tabs
   plone-keywords/history
   plone-keywords/index
   plone-keywords/login
   plone-keywords/reference-browser-widget
