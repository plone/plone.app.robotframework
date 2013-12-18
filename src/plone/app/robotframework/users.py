# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from zope.component.hooks import getSite
from plone.app.robotframework.remote import RemoteLibrary


class Users(RemoteLibrary):

    def create_user(self, username, *args, **kwargs):
        """Create user with given details and return its id"""
        # XXX: It seems that **kwargs does not yet work with Robot Framework
        # remote library interface and that's why we need to unpack the
        # keyword arguments from positional args list.
        roles = []
        properties = kwargs
        for arg in args:
            if not '=' in arg:
                roles.append(arg)
            else:
                name, value = arg.split('=', 1)
                if name in ('email', 'password'):
                    properties[name] = value
                else:
                    properties[name] = value
        if not 'email' in properties:
            properties['email'] = '%s@example.com' % username

        portal = getSite()
        registration = getToolByName(portal, 'portal_registration')
        portal_properties = getToolByName(portal, 'portal_properties')

        use_email_as_username =\
            portal_properties.site_properties.use_email_as_login

        user_id = use_email_as_username and properties['email'] or username
        password = properties.pop('password', username)
        roles = properties.pop('roles', ('Member', ))

        properties['username'] = user_id
        registration.addMember(
            user_id, password, roles, properties=properties)
