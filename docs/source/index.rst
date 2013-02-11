Plone ACT -- functional tests for Plone made easy
=================================================

**plone.act** and its documentation gives you everything to get started in
writing and executing functional Selenium tests (including acceptance tests)
for you Plone add-on.

**plone.act** peforms functional testing by using two testing frameworks:
`Robot Framework <http://code.google.com/p/robotframework/>`_ and
`Selenium <http://seleniumhq.org/>`_.

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

   Write a robot test for a new Plone add-on <templer>
   Write a robot test for an existing Plone add-on <tutorial>
   Learn more robot ... <robot>
   ... also by reading some good examples <https://github.com/plone/Products.CMFPlone/blob/master/Products/CMFPlone/tests/robot/robot_livesearch.txt>
   Debug robot tests <debugging>

.. If you are developing for Plone core and want information about
.. acceptance tests for Plone core skip to ADD-LINK-HERE.
..
.. Contents:
..
.. .. toctree::
..    :maxdepth: 2
..
..    robotsuite.rst
..    plone-keywords/index.rst
..    keywords.rst
..
.. Run single robot tests::
..
..   $ bin/test -s plone.app.deco -t Robot_Testcase_you_want_to_run


Print these
-----------

**How to write good Robot Frameowrk test cases**
    http://code.google.com/p/robotframework/wiki/HowToWriteGoodTestCases
**Robot Framework built-in library documentation**
    http://robotframework.googlecode.com/hg/doc/libraries/BuiltIn.html?r=2.7.6
**Robot Framework Selenium2Library documentation**
    http://rtomac.github.com/robotframework-selenium2library/doc/Selenium2Library.html


Become master
-------------

.. toctree::
   :maxdepth: 1
   :titlesonly:

   Speed up your test writing with ACT-server <server>
   Speed up your BDD Given-clauses with a remote library <remote>
