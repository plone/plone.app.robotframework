from plone.app.robotframework.remote import RemoteLibrary
from plone.app.robotframework.utils import disableCSRFProtection
from Products.PlonePAS.setuphandlers import activatePluginInterfaces
from Products.PluggableAuthService.plugins import DomainAuthHelper


class AutoLogin(RemoteLibrary):
    def enable_autologin_as(self, *args):
        """Add and configure DomainAuthHelper PAS-plugin to login
        all anonymous users from localhost as a special *Remote User* with
        one or more given roles. Examples of use::

            Enable autologin as  Manager
            Enable autologin as  Site Administrator
            Enable autologin as  Member  Contributor

        """
        disableCSRFProtection()
        if "robot_login" in self.acl_users.objectIds():
            self.acl_users.robot_login._domain_map.clear()
        else:
            DomainAuthHelper.manage_addDomainAuthHelper(self.acl_users, "robot_login")
            activatePluginInterfaces(self, "robot_login")
        user = ", ".join(sorted(args))
        self.acl_users.robot_login.manage_addMapping(
            match_type="regex", match_string=".*", roles=args, username=user
        )

    def set_autologin_username(self, username):
        """Update autologin mapping with the given username"""
        disableCSRFProtection()
        if "robot_login" not in self.acl_users.objectIds():
            raise Exception("Autologin is not enabled")
        if len(self.acl_users.robot_login._domain_map) == 0:
            raise Exception("Autologin is not enabled")
        domain_map_key = list(self.acl_users.robot_login._domain_map.keys())[0]
        domain_map = self.acl_users.robot_login._domain_map[domain_map_key]
        domain_map[0]["username"] = username
        self.acl_users.robot_login._domain_map[domain_map_key] = domain_map

    def disable_autologin(self):
        """Clear DomainAuthHelper's map to effectively 'logout' user
        after 'autologin_as'. Example of use::

            Disable autologin

        """
        if "robot_login" in self.acl_users.objectIds():
            disableCSRFProtection()
            self.acl_users.robot_login._domain_map.clear()
