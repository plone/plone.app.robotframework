# -*- coding: utf-8 -*-
from zope.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
from plone.app.robotframework.remote import RemoteLibrary
from Products.CMFPlone.utils import get_installer


class QuickInstaller(RemoteLibrary):

    def product_is_activated(self, product_name):
        """Assert that given product_name is activated (installed) in
        the add-ons control panel.
        """
        portal = getSite()
        qi = get_installer(portal)
        installed = qi.is_product_installed(product_name)
        portal_setup = getToolByName(portal, 'portal_setup')
        imported = portal_setup.getProfileImportDate(
            'profile-{0}:default'.format(product_name))
        assert installed or imported,\
            u"Product '{0}' was not activated.".format(product_name)

    product_is_installed = product_is_activated
