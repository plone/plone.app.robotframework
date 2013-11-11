Integrate with Travis-CI
========================

travis.cfg
----------

.. code-block:: ini

   [buildout]
   extends =
       https://raw.github.com/collective/buildout.plonetest/master/travis-4.x.cfg

   package-name = my.product
   package-extras = [test]

   allow-hosts +=
       code.google.com
       robotframework.googlecode.com


.travis.yml
-----------

.. code-block:: yaml

   language: python
   python: "2.7"
   install:
   - virtualenv test-env --no-setuptools
   - mkdir -p buildout-cache/downloads
   - test-env/bin/python bootstrap.py -c travis.cfg
   - bin/buildout -N -t 3 -c travis.cfg
   before_script:
   - export DISPLAY=:99.0
   - sh -e /etc/init.d/xvfb start
   script: bin/test


Build matrix
------------

.. code-block:: yaml

   env:
     matrix:
     - PLONE_VERSION=4.0
     - PLONE_VERSION=4.1
     - PLONE_VERSION=4.2
     - PLONE_VERSION=4.3


S3 artifacts
------------

.. code-block:: bash

   $ gem install travis
   $ travis encrypt ARTIFACTS_AWS_ACCESS_KEY_ID=... -r gh-user/my.product --add
   $ travis encrypt ARTIFACTS_AWS_SECRET_ACCESS_KEY=... -r gh-user/my.product--add

.. code-block:: yaml

   language: python
   python: '2.7'
   install:
   - virtualenv test-env --no-setuptools
   - mkdir -p buildout-cache/downloads
   - test-env/bin/python bootstrap.py -c travis.cfg
   - bin/buildout -N -t 3 -c travis.cfg
   before_script:
   - export DISPLAY=:99.0
   - sh -e /etc/init.d/xvfb start
   - gem install travis-artifacts
   after_script:
   - travis-artifacts upload --path parts/test
   script: bin/test
   env:
     global:
     - secure: ...
     - secure: ...
     - ARTIFACTS_S3_BUCKET=my.product
