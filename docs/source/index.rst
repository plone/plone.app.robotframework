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

So, you are building a brand new add-on for `Plone <http://www.plone.org/>`_
and would like to write some tests for it. Or, maybe you'd like to do it right
(tm) and write the sketch some tests before writing any code.

Welcome! ``plone.act`` holds all your need to test Plone or our add-on for it
using `Robot Framework <http://code.google.com/p/robotframework/>`_.

Robot Framework is a generic test automation framework for acceptance testing
and acceptance test-driven development (ATDD), even for behavior driven
development (BDD). It has easy-to-use plain text test syntax and utilizes the
keyword-driven testing approach.

``plone.act`` and this documentation gives you everything to get started in
writing and executing acceptance tests for you add-on.

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

Contents:

.. toctree::
   :maxdepth: 2

   plone-keywords/index.rst
   keywords.rst
   robotsuite.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
