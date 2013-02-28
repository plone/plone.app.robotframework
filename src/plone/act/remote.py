# -*- coding: utf-8 -*-
from OFS.SimpleItem import SimpleItem
from Products.PlonePAS.Extensions.Install import activatePluginInterfaces
from Products.PluggableAuthService.plugins import DomainAuthHelper


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

    def product_is_activated(self, product_name):
        """Assert that given product_name is activated in
        portal_quickinstaller.

        """
        from Products.CMFCore.utils import getToolByName
        quickinstaller = getToolByName(self, "portal_quickinstaller")
        assert quickinstaller.isProductInstalled(product_name),\
            "Product '%s' was not installed." % product_name

    def enable_autologin_as(self, *args):
        """Add and configure DomainAuthHelper PAS-plugin to login
        all anonymous users from localhost as a special *Remote User* with
        one or more given roles. Examples of use::

            Enable autologin as  Manager
            Enable autologin as  Site Administrator
            Enable autologin as  Member  Contributor

        """
        if "robot_login" in self.acl_users.objectIds():
            self.acl_users.robot_login._domain_map.clear()
        else:
            DomainAuthHelper.manage_addDomainAuthHelper(
                self.acl_users, "robot_login")
            activatePluginInterfaces(self, "robot_login")
        user = ", ".join(sorted(args))
        self.acl_users.robot_login.manage_addMapping(
            match_type="regex", match_string=".*", roles=args, username=user)

    def disable_autologin(self):
        """Clear DomainAuthHelper's map to effectively 'logout' user
        after 'autologin_as'. Example of use::

            Disable autologin

        """
        if "robot_login" in self.acl_users.objectIds():
            self.acl_users.robot_login._domain_map.clear()
