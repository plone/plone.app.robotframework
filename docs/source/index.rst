Plone ACT -- acceptance tests for Plone made easy
=================================================

``plone.act`` and this documentation gives you everything to get started in
writing and executing acceptance tests (funtional Selenium tests) for you
add-on or for Plone core.

Different developers may have different meanings for accectance tests but
within the Plone community when we talk about acceptance testing we are meaning
tests which check out the user interface or through the web testing.

``plone.act`` peforms acceptance testing by using two testing frameworks:
`Robot Framework <http://code.google.com/p/robotframework/>`_ and
`Selenium <http://seleniumhq.org/>`_.

Robot Framework is a generic test automation framework for acceptance testing
and acceptance test-driven development (ATDD), even for behavior driven
development (BDD). It has easy-to-use plain text test syntax and utilizes the
keyword-driven testing approach. Selenium is a web browser automation framework
that exercises the browser as if the user was interacting with the browser.

Next: :doc:`Get started by seeing an example of how to add acceptance tests to your
add-on. <tutorial.rst>`

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
