# -*- coding: utf-8 -*-
import os

from robot.libraries.BuiltIn import BuiltIn
from plone.app.robotframework.remote import RemoteLibrary


class I18N(RemoteLibrary):

    def _get_robot_variable(self, name):
        if getattr(BuiltIn(), '_context', None) is not None:
            return BuiltIn().get_variable_value('${%s}' % name, [])
        else:
            candidates = os.environ.get(name, '').split(',')
            return filter(bool, [s.strip() for s in candidates])[0]

    def set_default_language(self, language=None):
        """Change portal default language"""
        if language is None:
            language = os.environ.get('LANGUAGE') or 'en'
        setattr(self.portal_url.getPortalObject(), 'language', language)
        self.portal_languages.setDefaultLanguage(language)

    def translate(self, msgid, *args, **kwargs):
        """Return localized string for given msgid"""
        # XXX: It seems that **kwargs does not yet work with Robot Framework
        # remote library interface and that's why we need to unpack the
        # keyword arguments from positional args list.
        mapping = {}
        for arg in args:
            name, value = arg.split('=', 1)
            kwargs[name] = value
        for key, value in kwargs.items():
            if not key in ('target_language', 'domain', 'default'):
                mapping[key] = value
        if kwargs.get('target_language'):
            return translate(
                msgid, target_langauge=kwargs.get('target_language'),
                domain=kwargs.get('domain'),
                default=kwargs.get('default') or msgid, mapping=mapping)
        else:
            return translate(
                msgid, context=self.REQUEST, domain=kwargs.get('domain'),
                default=kwargs.get('default') or msgid, mapping=mapping)
