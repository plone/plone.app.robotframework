#!/bin/sh
LIBDOC="../bin/libdoc -F REST"

$LIBDOC --name="Plone User Keywords" plone/app/robotframework/keywords.robot source/libdoc/user_keywords.html
$LIBDOC --name="Zope2Server User Keywords" plone/app/robotframework/server.robot source/libdoc/user_server.html
$LIBDOC --name="Selenium User Keywords" plone/app/robotframework/selenium.robot source/libdoc/user_selenium.html
$LIBDOC --name="SauceLabs User Keywords" plone/app/robotframework/saucelabs.robot source/libdoc/user_saucelabs.html

$LIBDOC --name="Zope2Server Library" plone.app.robotframework.Zope2Server source/libdoc/python_zope2server.html
$LIBDOC --name="SauceLabs Library" plone.app.robotframework.SauceLabs source/libdoc/python_saucelabs.html
$LIBDOC --name="Debugging Library" plone.app.robotframework.Debugging source/libdoc/python_debugging.html
$LIBDOC --name="LayoutMath Library" plone.app.robotframework.LayoutMath source/libdoc/python_layoutmath.html

$LIBDOC --name="Zope2Server Remote Library" plone.app.robotframework.Zope2ServerRemote source/libdoc/remote_zope2server.html
$LIBDOC --name="AutoLogin Remote Library" plone.app.robotframework.AutoLogin source/libdoc/remote_autologin.html
$LIBDOC --name="GenericSetup Remote Library" plone.app.robotframework.GenericSetup source/libdoc/remote_genericsetup.html
$LIBDOC --name="I18N Remote Library" plone.app.robotframework.I18N source/libdoc/remote_i18n.html
$LIBDOC --name="MockMailHost Remote Library" plone.app.robotframework.MockMailHost source/libdoc/remote_mockmailhost.html
$LIBDOC --name="Users Remote Library" plone.app.robotframework.Users source/libdoc/remote_users.html
$LIBDOC --name="Content Remote Library" plone.app.robotframework.Content source/libdoc/remote_content.html
$LIBDOC --name="QuickInstaller Remote Library" plone.app.robotframework.QuickInstaller source/libdoc/remote_quickinstaller.html
