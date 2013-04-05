Writing Robot Framework tests for Plone
=======================================

.. warning::

    It's Plone Open Garden 2013 (from 3.4.2013 to 7.4.2013) and a lot of
    changes will be made during the event.

**plone.app.robotframework** provides `Robot Framework
<http://code.google.com/p/robotframework/>`_ compatible tools and resources for
writing functional Selenium tests (including acceptance tests) for Plone CMS
and its add-ons.

**This documentation** gives you everything to get started in writing and
executing functional Selenium tests (including acceptance tests) for Plone or
your own Plone add-on. It depends on two testing frameworks, `Robot Framework
<http://code.google.com/p/robotframework/>`_ and `Selenium
<http://seleniumhq.org/>`_ (with
`Selenium2Library <https://github.com/rtomac/robotframework-selenium2library>`_),
and uses the tools and resources provided by plone.app.robotframework.

Robot Framework is a generic test automation framework for acceptance testing
and acceptance test-driven development (ATDD), even for behavior driven
development (BDD). It has easy-to-use plain text test syntax and utilizes the
keyword-driven testing approach. Selenium is a web browser automation framework
that exercises the browser as if the user was interacting with the browser.


Start here
----------

.. toctree::
   :maxdepth: 1
   :titlesonly:

   Writing robot tests with plone.app.robotframework <happy>
   Learn more about robot <robot>
   Debug robot tests <debugging>

Print these
-----------

**Robot Framework built-in library documentation**
    http://robotframework.googlecode.com/hg/doc/libraries/BuiltIn.html?r=2.7.7
**Robot Framework Selenium2Library documentation**
    http://rtomac.github.com/robotframework-selenium2library/doc/Selenium2Library.html

Read more
---------

**How to write good Robot Framework test cases**
    http://code.google.com/p/robotframework/wiki/HowToWriteGoodTestCases

Old tutorials
-------------

.. toctree::
   :maxdepth: 1
   :titlesonly:

   Write a robot test for a new Plone add-on <templer>
   Write a robot test for an existing Plone add-on <tutorial>
   Speed up your test writing with robot-server <server>
   Speed up your BDD Given-clauses with a remote library <remote>
