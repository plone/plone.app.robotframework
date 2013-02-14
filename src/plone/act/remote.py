# -*- coding: utf-8 -*-
from OFS.SimpleItem import SimpleItem

from Products.PluggableAuthService.plugins import DomainAuthHelper
from Products.PlonePAS.Extensions.Install import activatePluginInterfaces


class RemoteKeywordsLibrary(SimpleItem):
    """Robot Framework Remote Library Tool for Plone

    See also: http://robotframework.googlecode.com/hg/doc/userguide/RobotFrameworkUserGuide.html?r=2.7.65#remote-library-interface

    """
    def get_keyword_names(self):
        """Return names of the implemented keywords
        """
        blacklist = dir(SimpleItem)
        blacklist.extend(['get_keyword_names', 'run_keyword'])
        names = filter(lambda x: x[0] != '_' and x not in blacklist, dir(self))
        return names

    def run_keyword(self, name, args):
        """Execute the specified keyword with given arguments.
        """
        func = getattr(self, name, None)
        result = {'error': '', 'return': ''}
        try:
            retval = func(*args)
        except Exception, e:
            result['status'] = 'FAIL'
            result['error'] = str(e)
        else:
            result['status'] = 'PASS'
            result['return'] = retval
        return result

    def product_has_been_activated(self, product_name):
        """Asserts that given product_name is activated in
        portal_quickinstaller.

        """
        from Products.CMFCore.utils import getToolByName
        quickinstaller = getToolByName(self, "portal_quickinstaller")
        assert quickinstaller.isProductInstalled(product_name),\
            "Product '%s' was not installed." % product_name

    def autologin_as(self, *args):
        """Adds and configures DomainAuthHelper PAS-plugin to login
        all anonymous users from localhost as a special *Remote User* with
        one or more given roles. Examples of use::

            Autologin as  Manager
            Autologin as  Site Administrator
            Autologin as  Member  Contributor

        """
        if "robot_login" in self.acl_users.objectIds():
            self.acl_users.robot_login._domain_map.clear()
        else:
            DomainAuthHelper.manage_addDomainAuthHelper(
                self.acl_users, "robot_login")
            activatePluginInterfaces(self, "robot_login")
        self.acl_users.robot_login.manage_addMapping(
            match_type="equals", match_string="localhost", roles=args)

    def logout_autologin(self):
        """Clears DomainAuthHelper's map to effectively 'logout' user
        after 'autologin_as'.
        """
        if "robot_login" in self.acl_users.objectIds():
            self.acl_users.robot_login._domain_map.clear()
