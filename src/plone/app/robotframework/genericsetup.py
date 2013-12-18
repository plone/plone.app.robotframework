# -*- coding: utf-8 -*-
from plone.app.robotframework.remote import RemoteLibrary


class GenericSetup(RemoteLibrary):

    def apply_profile(self, name):
        """Apply named profile"""
        from Products.CMFCore.utils import getToolByName
        portal_setup = getToolByName(self, 'portal_setup')
        portal_setup.runAllImportStepsFromProfile('profile-%s' % name)
