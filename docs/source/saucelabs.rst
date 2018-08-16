Integrate with Sauce Labs
=========================

1. Register an account for http://saucelabs.com/ with the *Open Sauce* plan.
   Derive username from product name. For example, ``myproduct``. Use your own
   contact email for the beginning.  It can be changed later.

2. Install travis-gem for your active Ruby-installation:

   .. code-block:: bash

      $ sudo gem install travis

3. Log in to Sauce Labs to see your Sauce Labs access key (at the bottom of
   the left column).

4. Encrypt Sauce Labs credentials into ``.travis.yml``:

   .. code-block:: bash

      $ travis encrypt SAUCE_USERNAME=... -r github-user-or-organization/myproduct --add
      $ travis encrypt SAUCE_ACCESS_KEY=... -r github-user-or-organization/myproduct --add

5. Update ``.travis.yml`` to set up the Sauce Labs connection before tests:

   .. code-block:: yaml

      [...]
      addons:
        sauce_connect:
        - username: $SAUCE_USERNAME
        - access_key: $SAUCE_ACCESS_KEY
      [...]
      env:
        [...]
        global:
        - secure: ...
        - secure: ...
        - ROBOT_BUILD_NUMBER=travis-$TRAVIS_BUILD_NUMBER
        - ROBOT_REMOTE_URL=http://$SAUCE_USERNAME:$SAUCE_ACCESS_KEY@ondemand.saucelabs.com:80/wd/hub
        - ROBOT_DESIRED_CAPABILITIES=tunnel-identifier:$TRAVIS_JOB_NUMBER
      [...]

.. note:: If you already have an ``env`` section, for instance to define
   different versions of Plone like this:

   .. code-block:: yaml

      env:
      - PLONE_VERSION=5.0
      - PLONE_VERSION=5.1
      - PLONE_VERSION=5.2

   you will need to declare those variables in a ``matrix`` section, like this:

   .. code-block:: yaml

      env:
        matrix:
        - PLONE_VERSION=5.0
        - PLONE_VERSION=5.1
        - PLONE_VERSION=5.2
        global:
        - secure: ...
        - secure: ...
        - ROBOT_BUILD_NUMBER=travis-$TRAVIS_BUILD_NUMBER
        - ROBOT_REMOTE_URL=http://$SAUCE_USERNAME:$SAUCE_ACCESS_KEY@ondemand.saucelabs.com:80/wd/hub
        - ROBOT_DESIRED_CAPABILITIES=tunnel-identifier:$TRAVIS_JOB_NUMBER

6. Update your test suites to use SauceLabs test browser by including
   ``saucelabs.robot`` resource and updating your *Test Setup* and *Test
   Teardown* to use SauceLabs-supporting keywords (with these changes
   the test suites will still continue to work also without SauceLabs):

   .. code-block:: robotframework

      *** Settings ***

      Force Tags  wip-not_in_docs
      ...

      Resource  plone/app/robotframework/saucelabs.robot

      Test Setup  Open SauceLabs test browser
      Test Teardown  Run keywords  Report test status  Close all browsers

      ...

7. Update ``travis.cfg`` to allow downloading robotframework-packages:

   .. code-block:: ini

      [buildout]

      ...

      allow-hosts +=
          code.google.com
          robotframework.googlecode.com


Running Sauce Labs build manually
---------------------------------

1. Download and unzip http://saucelabs.com/downloads/Sauce-Connect-latest.zip,
   then start Sauce-Connect with:

   .. code-block:: bash

      $ java -jar Sauce-Connect.jar <your_sauce_username> <your_sauce_accesskey> -i manual

2. Start ``bin/robot-server``:

   .. code-block:: bash

      $ bin/robot-server my.product.testing.ROBOT_TESTING

3. Run tests with ``bin/robot``:

   .. code-block:: bash

      $ bin/robot -v REMOTE_URL:http://SAUCE_USERNAME:SAUCE_ACCESS_KEY@ondemand.saucelabs.com:80/wd/hub -v BUILD_NUMBER:manual -v DESIRED_CAPABILITIES:tunnel-identifier:manual src/my/product/tests/test_product.robot

or

4. Create an argument file, e.g. ``saucelabs_arguments.txt``:

   .. code-block:: bash

      -v REMOTE_URL:http://SAUCE_USERNAME:SAUCE_ACCESS_KEY@ondemand.saucelabs.com:80/wd/hub
      -v BUILD_NUMBER:manual
      -v DESIRED_CAPABILITIES:tunnel-identifier:manual

5. Execute ``bin/robot`` with the argument file option:

   .. code-block:: bash

      $ bin/robot -A saucelabs_arguments.txt src/my/product/tests/test_product.robot
