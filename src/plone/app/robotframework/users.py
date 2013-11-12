# -*- coding: utf-8 -*-
from plone import api
from plone.app.robotframework.remote import RemoteLibrary


class Users(RemoteLibrary):

    def create_user(self, username, *args, **kwargs):
        """Create user with given details and return its id"""
        # XXX: It seems that **kwargs does not yet work with Robot Framework
        # remote library interface and that's why we need to unpack the
        # keyword arguments from positional args list.
        roles = []
        properties = {}
        for arg in args:
            if not '=' in arg:
                roles.append(arg)
            else:
                name, value = arg.split('=', 1)
                if name in ('email', 'password'):
                    kwargs[name] = value
                else:
                    properties[name] = value
        if not 'email' in kwargs:
            kwargs['email'] = '%s@example.com' % username
        return api.user.create(
            username=username, roles=roles, properties=properties, **kwargs)
