# -*- coding: utf-8 -*-
from plone.app.robotframework.remote import RemoteLibrary
from plone.app.robotframework.utils import disableCSRFProtection


class GenericSetup(RemoteLibrary):

    def apply_profile(self, name):
        """Apply named profile"""
        disableCSRFProtection()
        from Products.CMFCore.utils import getToolByName
        portal_setup = getToolByName(self, 'portal_setup')
        portal_setup.runAllImportStepsFromProfile('profile-%s' % name)

    def apply_profile_step(self, name, step):
        """Apply step from named profile"""
        disableCSRFProtection()
        from Products.CMFCore.utils import getToolByName
        portal_setup = getToolByName(self, 'portal_setup')
        portal_setup.runImportStepFromProfile('profile-%s' % name, step)
