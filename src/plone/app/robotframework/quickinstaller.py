# -*- coding: utf-8 -*-
from plone.app.robotframework.remote import RemoteLibrary


class QuickInstaller(RemoteLibrary):

    def product_is_activated(self, product_name):
        """Assert that given product_name is activated (installed) in
        portal_quickinstaller.
        """
        from Products.CMFCore.utils import getToolByName
        quickinstaller = getToolByName(self, 'portal_quickinstaller')
        assert quickinstaller.isProductInstalled(product_name),\
            u"Product '%s' was not activated." % product_name

    product_is_installed = product_is_activated
