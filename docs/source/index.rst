.. warning::
     If you are reading this on GitHub, DON'T! Read this on
     `ReadTheDocs <http://ploneact.readthedocs.org/en/latest/index.html>`_
     so you have working references and proper formatting.

.. warning::
     This package is still under heavy development. Do not use it yet unless
     you are completely sure what you are doing.

======================
Plone Acceptance Tests
======================

``plone.act`` and this documentation gives you everything to get started in
writing and executing acceptance tests for you add-on or for Plone core.

Different developers may have different meanings for accectance tests but within
the Plone community when we talk about acceptance testing we are meaning tests
which check out the user interface or through the web testing.

``plone.act`` peforms acceptance testing by using two testing frameworks:
`Robot Framework <http://code.google.com/p/robotframework/>`_ and `Selenium <http://seleniumhq.org/>`_.

Robot Framework is a generic test automation framework for acceptance testing
and acceptance test-driven development (ATDD), even for behavior driven
development (BDD). It has easy-to-use plain text test syntax and utilizes the
keyword-driven testing approach. Selenium is a web browser automation framework that
exercises the browser as if the user was interacting with the browser.

Let's get started by seeing an example of how to add acceptance tests to your add-on. 
If you are developing for Plone core and want information about acceptance tests for
Plone core skip to ADD-LINK-HERE.

Contents:

.. toctree::
   :maxdepth: 2

   robotsuite.rst
   plone-keywords/index.rst
   keywords.rst

Run single robot tests::

  $ bin/test -s plone.app.deco -t Robot_Testcase_you_want_to_run

Todo-List:

- Describe and document the two possible test runner approaches (asko's and godfroid's)
- Describe/investigate different ways of writing higher-level Plone keywords (standard robot vs. BDD, given-when-then)
- Write documentation for selenium2library keywords (tisto).
- Write documentation for Plone keywords. (Should we use robot framework tools to do this and then simply reference them? Ed)
- Write documentation about separating Keywords and Tests
  - What is the difference between a keyword and a test
  - Keywords should be for test setup or running, but should not themselves
    test things.  This way failures will be pointing to functionality and not
    be across multiple tests.

Wish List:

- Add support for jQuery like selectors in selenium (http://code.google.com/p/robotframework-seleniumlibrary/wiki/jQueryElementSelectors
https://github.com/rtomac/robotframework-selenium2library/issues/77)

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
