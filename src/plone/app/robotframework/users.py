from plone.app.robotframework.remote import RemoteLibrary
from plone.app.robotframework.utils import disableCSRFProtection
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import ISecuritySchema
from zope.component import getUtility
from zope.component.hooks import getSite


class Users(RemoteLibrary):
    def create_user(self, *args, **kwargs):
        """Create user with given details and return its id"""
        disableCSRFProtection()
        # FIXME: we are alrady using robotframework = 3.0
        # XXX: Because kwargs are only supported with robotframework >= 2.8.3,
        # we must parse them here to support robotframework < 2.8.3.
        for arg in [x for x in args if "=" in x]:
            name, value = arg.split("=", 1)
            kwargs[name] = value

        assert len(args), "username must be provided."
        username = args[0]

        roles = []
        properties = kwargs
        for arg in [x for x in args[1:] if "=" not in x]:
            roles.append(arg)

        if "email" not in properties:
            properties["email"] = "%s@example.com" % username

        portal = getSite()
        registration = getToolByName(portal, "portal_registration")
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISecuritySchema, prefix="plone")
        use_email_as_username = getattr(settings, "use_email_as_login", None)
        user_id = use_email_as_username and properties["email"] or username
        password = properties.pop("password", username)

        roles.extend(properties.pop("roles", []))
        if not roles:
            roles.append("Member")
        properties["username"] = user_id
        registration.addMember(user_id, password, roles, properties=properties)
