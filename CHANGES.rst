Changelog
=========

0.9.17 (2016-07-15)
-------------------

Breaking changes:

- *add item here*

New features:

- Test with robotframework version 3.0.   [maurits]

- Added ``Plone Test Setup`` and ``Plone Test Teardown`` keywords.  In
  that last one, in case of a failure do what is done by
  ``run_on_failure``, which will be removed in version 1.0.  This
  means a screen shot by default, but you can override this on the
  command line with for example ``ROBOT_SELENIUM_RUN_ON_FAILURE=Debug``.
  See https://github.com/plone/Products.CMFPlone/pull/1652
  [maurits]

- Add ``Running tests with the Google Chrome browser`` section.
  Briefly: ``ROBOT_BROWSER=chrome ./bin/test --all``
  [thet]

Bug fixes:

- Replaced deprecated ``Fail Unless Equal`` with ``Should Be Equal``
  in test.  [maurits]


0.9.16 (2016-06-07)
-------------------

Fixes:

- Removed bad format parameter on ObjectModifiedEvent: must be an Attributes instance.
  See zope.lifecycleevent.ObjectModifiedEvent class.
  Removed because we can't get the interface and the correct fieldname.
  [sgeulette]

0.9.15 (2016-02-26)
-------------------

Fixes:

- Do not require argparse, decorator, and simplejson in Python 2.7,
  only lower.  [maurits]

- Replace import of ``zope.testing.testrunner`` with ``zope.testrunner``.
  [thet]


0.9.14 (2015-10-11)
-------------------

- With lazy sandbox-server shutdown, let test layers to declare themselves
  dirty and force sandbox rebuild when required
  [datakurre]

- Fix PloneRobotFixture to know its deployment state and declare itself
  dirty when required for lazy sandbox-server shutdown support
  [datakurre]

0.9.13 (2015-10-10)
-------------------

- Add support for lazy sandbox-server (Zope2Server) shutdown with
  ``pybot --listener plone.app.framework.server.LazyStop`` or with
  Sphinx extension ``plone.app.robotframeworks.server`` to allow
  sequential Sphinx documents to share the same server for screenshots
  generation
  [datakurre]

0.9.12 (2015-09-27)
-------------------

- Fix CSRF errors on content creation keywords
  [vangheem]


0.9.11 (2015-09-16)
-------------------

- Fix issue where 'use_email_as_login' was not found in registry
  [datakurre]
- Fix selenium2library link in documentation
  [gotcha]
- Inline sample robot code for mentioned example into docs
  [pjoshi]

0.9.10 (2015-07-30)
-------------------

- Update good known versions.
  [gotcha]

- "Create content" keyword fix: creation of random images in ATCT did not
  work when dexterity was installed.
  [gotcha]


0.9.9 (2015-03-13)
------------------

- "Create content" keyword fixes: Fix creation of random images, add image to
  News Item if not defined, add file to File if not defined.
  [thet]

- Also detect mockup-based modals in the "Click Overlay Link" and
  "Click Overlay Button" keywords.
  [davisagli]

- Read ``use_email_as_login`` setting from the registry instead of portal
  properties (see https://github.com/plone/Products.CMFPlone/issues/216).
  [jcerjak]


0.9.8 (2014-11-11)
------------------

- Fix dependency on plone.namedfile to be optional
  [hvelarde, datakurre]

0.9.7 (2014-10-13)
------------------

- Restore robotsuite into direct dependencies for convenience
  [datakurre]

0.9.6 (2014-10-11)
------------------

- Fix package dependencies; Remove needless dependency on unittest2 Remove
  implicit dependency on z3c.relationfield unless it's required by the tested
  add-on
  [vincentfretin, hvelarde, datakurre]

0.9.5 (2014-10-09)
------------------

- Fix issue where Dexterity content creation without explicit id fails
  [datakurre]
- Add user keywords 'a logged in test user' and 'a logged in site owner'.
  [tisto]
- Add user.robot keywords.
  [tisto]
  [datakurre]
- Refactor Dexterity not to be explicit dependency
  [datakurre]
- Add default RobotRemote instance to support enabling the default remote
  library with collective.monkeypatcher (see p.a.robotframework.testing)
  [datakurre]

0.9.4 (2014-06-23)
------------------

- Make the 'id' parameter optional for the 'create content' keyword.
  [timo]

0.9.3 (2014-06-23)
------------------

- Add 'Global allow' content keyword
  [tisto]

0.9.2 (2014-04-28)
------------------

- Fix package dependencies
  [hvelarde]

0.9.1 (2014-04-16)
------------------

- Fix robot-server debug-mode support to work also in code reloading mode
  [datakurre]

0.9.0 (2014-04-13)
------------------

- Add a new command-line option for robot-server to start Zope in debug-mode
  (useage: bin/robot-server -d or bin/robot-server --debug-mode)
  [datakurre]
- Change robot LISTENER_PORT (used in communication between bin/robot-server
  and bin/robot via robotframework) to default port 49999 instead of 10001
  [datakurre]
- Add SELENIUM_RUN_ON_FAILURE-variable into resource file
  plone/app/robotframewor/selenium.robot to support custom keyword be called
  at the first failing step (defaults to Capture Page Screenshot, but can be
  changed to ease debugging)
- Refactor Debug keyword in plone/app/robotframwork/keywords.robot to
  to support both DebugLibrary and Dialogs-library and finally fallback to
  pdb REPL.
- Add new script bin/robot-debug as a shortcut to run robot with variable
  SELENIUM_RUN_ON_FAILURE=Debug
  [datakurre]
- Fix MOCK_MAILHOST_FIXTURE's teardown to don't crash on missing
  portal._original_mailhost attribute because of wrong layer order
  [thet]

0.8.5 (2014-04-02)
------------------

- Add 'Get total amount of sent emails'-keyword into MockMailHost remote
  library
  [datakurre]

0.8.4 (2014-03-31)
------------------

- Fix regression in PloneRobotFixture (used in documentation screenshots)
  [datakurre]

0.8.3 (2014-03-04)
------------------

- Fix 'title'-keyword argument to be optional for Create content -keyword
  [datakurre]

0.8.2 (2014-02-17)
------------------

- Move robotframework-debuglibrary into its own extras to not require it by
  default and to restore compatibility with robotframework < 2.8.
  **Note:** *Debug*-keywords now requires either that
  *plone.app.robotframework* is required with **[debug]** extras or that
  *robotframework-debuglibrary* is requires explicitly.
  [datakurre]

0.8.1 (2014-02-13)
------------------

- Fix debug-keyword to load DebugLibrary lazily to not require readline until
  its really required [fixes #20]
  [datakurre]

0.8.0 (2014-02-13)
------------------

- Add Debug-keyword by adding dependency on robotframework-debuglibrary and
  automatically include it in keywords.robot.
  [datakurre]

0.7.5 (2014-02-11)
------------------

- Fix crete content keyword to support schema.Object-fields (e.g. RichText)
  [datakurre]
- Fix support of passing list variables from environment into PloneRobotFixture
  [datakurre]

0.7.4 (2014-02-11)
------------------

- Add 'Delete content' keyword for content remote library
  [datakurre]

0.7.3 (2014-02-09)
------------------

- Allow to custom open browser keyword in server.robot
  [datakurre]

0.7.2 (2014-02-09)
------------------

- Add support for registering translations directly from docs for screenshots
  [datakurre]

0.7.1 (2014-02-08)
------------------

- Add ignored Sphinx-directives to pybot to make it easier to run pybot agains
  Sphinx documentation
  [datakurre]
- Update libdoc-generated documentations
  [datakurre]

0.7.0 (2014-02-08)
------------------

- Fix kwargs support for robotframework >= 2.8.3 [fixes #17]
  [datakurre]
- Add path_to_uid method to content library.
  [tisto]
- Add content library container tests for documentation.
  [tisto]
- The title attribute for Dexterity types needs to be unicode.
  [tisto]
- Add field type reference (only intid support for now).
  [tisto]
- Add file/image support to set_field_value method/keyword.
  [tisto]
- Add support for list type.
  [tisto]
- Support setting RichText (Dexterity only).
  [tisto]
- Call reindexObject after setting a field value so the object is updated in
  the catalog as well.
  [tisto]
- Add new set_field_value keyword that allows to set the field type explicitly.
  [tisto]
- Fix use object_rename view instead of pop-up for rename content title
  [Gagaro]
- Fix use "a" instead of "span" for Open User Menu
  [Gagaro]
- Fix rename content title
  [Gagaro]

0.7.0rc4 (2013-11-13)
---------------------

- Add support for path as container argument value in Create content -keyword
  [datakurre]

0.7.0rc3 (2013-11-12)
---------------------

- Drop dependency on plone.api
  [datakurre]

0.7.0rc2 (2013-11-12)
---------------------

- Fix backwards compatibility with robotframework 1.7.7
  [datakurre]

0.7.0rc1 (2013-11-10)
---------------------

This is Arnhem Sprint preview release of 0.7.0.

- Refactor and clean; Rename 'Do transition' to 'Fire transition';  Split
  'PloneAPI' RemoteLibrary into 'Content' and 'Users' libraries
  [datakurre]
- Add 'Pause'-keyword
  [datakurre]
- Cleanup Zope2ServerRemote-library keywords
  [datakurre]
- Add I18N, MockMailHost, PortalSetup and PloneAPI -keywords from c.usermanual
  [datakurre]
- Rename RemoteServer-keyword library into Zope2ServerRemote and provide a
  shortcut import
  [datakurre]
- Fix to support explicit layers with zodb_setup and zodb_teardown calls,
  because sometime the layers is not available (because of different server
  library instance); Add remote library for zodb_setup and zodb_teardown
  keywords
  [datakurre]
- Rename PloneRobotSandboxLayer into PloneRobotFixture, because it's only
  usable as it is
  [datakurre]
- Drop LiveSearch-layer (it was CMFPlone-specific); Add MockMailHostlayer; Add
  robot configurable PloneRobotSandboxLayer
  [datakurre]
- Refactor to use python only for environment variables and define other
  variables in robot to support robot variable overrides
  [datakurre]
- Deprecate annotate-library in favor of Selenium2Screenshots-library
  [datakurre]
- Remove moved CMFPlone-tests
  [datakurre]
- Use robotframework 2.8.1
  [datakurre]
- Fix to tell in 'robot-server' help how to enable code-reloading support
  [fixes #13]
  [datakurre]
- Add entry point for robot.libdoc
  [Benoît Suttor]
- Return location to reference new content
  [Benoît Suttor]
- Refactor add content keywords
  [Benoît Suttor]
- Explain stop keyword from debugging library
  [Benoît Suttor]

0.6.4 (2013-08-19)
------------------

- Better support for Login/Logout on multilingual sites by not relying on
  'Log in' and 'Log out' on these pages. Check css locators instead.
  [saily]

0.6.3 (2013-06-28)
------------------

- ZSERVER_PORT, ZOPE_HOST and ZOPE_PORT environment variables are supported.
  [gotcha]

- Make ``robot-server`` show ``logging`` messages.
  [gotcha]

0.6.2 (2013-06-19)
------------------

- Remove the default selenium-version (SELENIUM_VERSION-variable) set for
  sessions Sauce Labs to fix issues with mobile browser testing
  (selenium-version must not be set when testing mobile browsers)
  [datakurre]
- Documentation updates
  [gotcha, datakurre]
- Add ``Capture viewport screenshot`` into annotate.robot keywords library
  [datakurre]
- Fix Speak-keyword to use ``jQuery`` instead of ``jq``
  [datakurre]

0.6.1 (2013-05-16)
------------------

- Fix ``Click Action by`` keyword. on Sunburst Theme the action id is
  #plone-contentmenu-actions-${name}
  [JeanMichel FRANCOIS]
- Enhance Server-library to support carefully designed additional layers
  (appended after the main layer)
  [datakurre]
- Documentatio updates
  [ebrehault, Fulvio Casali, saily]

0.6.0 (2013-04-30)
------------------

- Add verbose console outout for robot-server for test setup and teardown
  [datakurre]
- Documentation update
  [datakurre, Silvio Tomatis]
- Merge pull request #2 from silviot/patch-1
- Add ``Element should become visible`` keyword
  [datakurre]

0.5.0 (2013-04-09)
------------------

- Add ``Align elements horizontally`` annotation keyword.

0.4.4 (2013-04-09)
------------------

- Fix image cropping math.

0.4.3 (2013-04-08)
------------------

- Fix the default Selenium timeout to be 30s instead of 10s, because
  defaults need to be safe at first and only then optimal.

0.4.2 (2013-04-08)
------------------

- Use ``Capture and crop page screenshot`` keyword in screencast example; Try
  more transparent annotation pointer

0.4.1 (2013-04-08)
------------------

- Rename ``Add dot`` to ``Add pointer`` and ``Add numbered dot`` to ``Add dot``;
  Available annotations keywords are now ``Add pointer``, ``Add dot`` and
  ``Add note``.

0.4.0 (2013-04-08)
------------------

- Moved speak.js into collective.js.speakjs.
- Add note positions. Add numbered dot
- Tune old annotation keywords.

0.3.0 (2013-04-07)
------------------

- Add annotation library with dot and note
- Add image cropping keyword into annotation library
- Restore pybot-entrypoint (it's needed for screenshot-usecase)

0.2.5 (2013-04-05)
------------------

- PLOG2013 development release.
- Fix Sauce Labs -library to work without tunnel identifier

0.2.4 (2013-04-04)
------------------

- PLOG2013 development release.
- Fix typo in AUTOLOGIN_LIBRARY_FIXTURE

0.2.3 (2013-04-04)
------------------

- PLOG2013 development release.
- Define dedicated re-usable AUTOLOGIN_ROBOT_FIXTURE
- Drop BBB for plone.act
- Drop entrypoints for pure pybot and rebot to make it easier to use them pure
  without extra dependencies by installing robotentrypoints-package

0.1.0 (2013-04-03)
------------------

- PLOG2013 development release.
