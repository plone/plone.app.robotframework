# -*- coding: utf-8 -*-
from plone.app.robotframework.remote import RemoteLibrary


class PortalSetup(RemoteLibrary):

    def apply_profile(self, name):
        """Apply named profile"""
        self.portal_setup.runAllImportStepsFromProfile('profile-%s' % name)
