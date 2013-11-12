# -*- coding: utf-8 -*-
from zope.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
from plone.app.robotframework.remote import RemoteLibrary


class QuickInstaller(RemoteLibrary):

    def product_is_activated(self, product_name):
        """Assert that given product_name is activated (installed) in
        portal_quickinstaller.
        """
        portal = getSite()
        portal_quickinstaller = getToolByName(portal, 'portal_quickinstaller')
        portal_setup = getToolByName(portal, 'portal_setup')

        installed = portal_quickinstaller.isProductInstalled(product_name)
        imported = portal_setup.getProfileImportDate('profile-%s:default' %
                                                     product_name)
        assert installed or imported,\
            u"Product '%s' was not activated." % product_name

    product_is_installed = product_is_activated
