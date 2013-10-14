Integrate with Sauce Labs
-------------------------

1. Register an account for http://saucelabs.com/ with the *Open Sauce* plan.
   Derive username from product name. For example, ``myproduct``. Use your own
   contact email for the beginning.  It can be changed later.

2. Install travis-gem for your active Ruby-installation::

       $ sudo gem install travis

3. Log in to Sauce Labs to see your Sauce Labs access key (at the bottom of
   the left column).

4. Encrypt Sauce Labs credentials into ``.travis.yml``::

       $ travis encrypt SAUCE_USERNAME=myusername -r mygithubname/myproduct --add env.global
       $ travis encrypt SAUCE_ACCESS_KEY=myaccesskey -r mygithubname/myproduct --add env.global

5. Update ``.travis.yml`` to set up the Sauce Labs connection before tests::

       ---
       language: python
       python: '2.7'
       install:
       - mkdir -p buildout-cache/downloads
       - python bootstrap.py -c travis.cfg
       - bin/buildout -N -t 3 -c travis.cfg
       - curl -O http://saucelabs.com/downloads/Sauce-Connect-latest.zip
       - unzip Sauce-Connect-latest.zip
       - java -jar Sauce-Connect.jar $SAUCE_USERNAME $SAUCE_ACCESS_KEY -i $TRAVIS_JOB_ID -f CONNECTED &
       - JAVA_PID=$!
       - bash -c "while [ ! -f CONNECTED ]; do sleep 2; done"
       script: bin/test
       after_script:
       - kill $JAVA_PID
       env:
         global:
         - secure: ! (here's an encrypted variable created with travis-commmand)
         - secure: ! (here's an encrypted variable created with travis-commmand)
         - ROBOT_BUILD_NUMBER=travis-$TRAVIS_BUILD_NUMBER
         - ROBOT_REMOTE_URL=http://$SAUCE_USERNAME:$SAUCE_ACCESS_KEY@ondemand.saucelabs.com:80/wd/hub
         - ROBOT_DESIRED_CAPABILITIES=tunnel-identifier:$TRAVIS_JOB_ID

.. note:: If you already have an ``env`` section, for instance to define
different versions of Plone like this::

       env:
         - PLONE_VERSION=4.0
         - PLONE_VERSION=4.1
         - PLONE_VERSION=4.2
         - PLONE_VERSION=4.3

   you will need to declare those variables in a ``matrix`` section, like this::

       env:
         matrix:
           - PLONE_VERSION=4.0
           - PLONE_VERSION=4.1
           - PLONE_VERSION=4.2
           - PLONE_VERSION=4.3
         global:
         - secure: ! (here's an encrypted variable created with travis-commmand)
         - secure: ! (here's an encrypted variable created with travis-commmand)
         - ROBOT_BUILD_NUMBER=travis-$TRAVIS_BUILD_NUMBER
         - ROBOT_REMOTE_URL=http://$SAUCE_USERNAME:$SAUCE_ACCESS_KEY@ondemand.saucelabs.com:80/wd/hub
         - ROBOT_DESIRED_CAPABILITIES=tunnel-identifier:$TRAVIS_JOB_ID

6. Update the test to use SauceLabs test browser::

       *** Settings ***

       ...

       Resource  plone/app/robotframework/saucelabs.robot

       Test Setup  Open SauceLabs test browser
       Test Teardown  Run keywords  Report test status  Close all browsers

       ...

7. Update ``travis.cfg`` to allow downloading robotframework-packages::

       [buildout]

       ...

       allow-hosts +=
           code.google.com
           robotframework.googlecode.com

.. note:: If you don't have Travis-CI-integration yet, you need to add ``travis.cfg``
for the above ``.travis.yml`` to work::

       [buildout]
       extends = https://raw.github.com/collective/buildout.plonetest/master/travis-4.x.cfg

       package-name = my.product
       package-extras = [test]

       allow-hosts +=
           code.google.com
           robotframework.googlecode.com

       [environment]
       ZSERVER_PORT = 8080
       ROBOT_ZOPE_PORT = 8080

       [test]
       environment = environment

   The *environment*-part and line in *test*-part are optional, but are
   required to run tests using Internet Explorer and mobile browsers
   using SauceLabs because SauceLabs proxies only
   `predefined sets of ports <https://saucelabs.com/docs/connect#localhost>`_.

Running sauce labs build manually
---------------------------------

0. Download and unzip http://saucelabs.com/downloads/Sauce-Connect-latest.zip, then start Sauce-Connect with::

       java -jar Sauce-Connect.jar <your_sauce_username> <your_sauce_accesskey> -i manual

1. Start ``bin/robot-server``::

       $ bin/robot-server my.product.testing.ROBOT_TESTING

2. Run tests with ``bin/robot``::

       $ bin/robot -v REMOTE_URL:http://SAUCE_USERNAME:SAUCE_ACCESS_KEY@ondemand.saucelabs.com:80/wd/hub -v BUILD_NUMBER:manual -v DESIRED_CAPABILITIES:tunnel-identifier:manual src/my/product/tests/test_product.robot

or

2. Create an argument file, e.g. ``saucelabs_arguments.txt``::

       -v REMOTE_URL:http://SAUCE_USERNAME:SAUCE_ACCESS_KEY@ondemand.saucelabs.com:80/wd/hub
       -v BUILD_NUMBER:manual
       -v DESIRED_CAPABILITIES:tunnel-identifier:manual

3. Execute ``bin/robot`` with the argument file option::

       bin/robot -A saucelabs_arguments.txt src/my/product/tests/test_product.robot

