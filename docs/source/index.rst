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
   robot

.. _zope.testrunner: http://pypi.python.org/pypi/zope.testrunner


Print these
-----------

Print these keyword libraries to be easily available when writing Robot
Framework tests, because they provide the basic building blocks for your
tests:

* `Robot Framework built-in library documentation`__
* `Robot Framework Selenium2Library documentation`__

__ http://robotframework.org/robotframework/latest/libraries/BuiltIn.html
__ http://robotframework.org/Selenium2Library/Selenium2Library.html


Advanced topics
---------------

.. toctree::
   :maxdepth: 1
   :titlesonly:

   debugging
   travis-ci
   saucelabs
   reload
   ride


User keywords
-------------

*plone.app.robotframework* ships with the following user keyword libraries
as resource files:

- :download:`libdoc/user_keywords.html`
- :download:`libdoc/user_saucelabs.html`
- :download:`libdoc/user_selenium.html`
- :download:`libdoc/user_server.html`

Each user keyword library can be included as a resource with ``Resource
plone/app/robotframework/libraryname.rst`` in test suite ``*** Settings ***``.


Remote keywords
---------------

Remote keywords are a special *plone.app.robotframework*-way to implement
Plone-specific keyword in Python for e.g. creating Plone content in test setup
keywords. *plone.app.robotframework* comes with the following remote keyword
libraries:

- :download:`libdoc/remote_autologin.html`
- :download:`libdoc/remote_content.html`
- :download:`libdoc/remote_genericsetup.html`
- :download:`libdoc/remote_i18n.html`
- :download:`libdoc/remote_mockmailhost.html`
- :download:`libdoc/remote_quickinstaller.html`
- :download:`libdoc/remote_users.html`
- :download:`libdoc/remote_zope2server.html`

All remote keywords above are included by including a special test fixture
``plone.app.robotframework.testing.REMOTE_LIBRARY_BUNDLE_FIXTURE`` in *bases*
of the used functional testing fixture, and finally with ``Library  Remote
${PLONE_URL}/RobotRemote``-command in test suite ``*** Settings ***``.

See ``testing.py`` in *plone.app.robotframework* for how to create a custom
remote library bundle fixture with only selected (or custom) remote keyword
libraries.


Python keywords
---------------

In addition to user keywords and remote libraries, *plone.app.robotframeworks*
provides the following generic Python keyword libraries (their code is not
dependent on Plone code base).

- :download:`libdoc/python_debugging.html`
- :download:`libdoc/python_layoutmath.html`
- :download:`libdoc/python_saucelabs.html`
- :download:`libdoc/python_zope2server.html`

Each Python keyword library can be included as with ``Library
plone.app.robotframework.LibraryClassName`` in test suite ```*** Settings
***``.


Other resources
---------------

* `How to write good Robot Framework test cases`__
* `List of available Robot Framework test libraries`__
* :doc:`plone.app.robotframework examples of use <examples>`

__ https://github.com/robotframework/HowToWriteGoodTestCases/blob/master/HowToWriteGoodTestCases.rst
__ http://robotframework.org/#libraries


Old tutorials
-------------

.. note:: While these tutorials are still useful for gettings started with
   Robot Framework testing for Plone, these may contain outdated instructions!

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
