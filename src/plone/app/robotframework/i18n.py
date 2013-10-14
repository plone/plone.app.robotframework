# -*- coding: utf-8 -*-
import os

from plone import api
from plone.app.robotframework.remote import RemoteLibrary

from zope.i18n import translate


class I18N(RemoteLibrary):

    def set_default_language(self, language=None):
        """Change portal default language"""
        portal_object = api.portal.get()
        if language is None:
            language = os.environ.get('LANGUAGE') or 'en'
        setattr(portal_object, 'language', language)
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
                domain=kwargs.get('domain') or 'plone',
                default=kwargs.get('default') or msgid, mapping=mapping)
        else:
            # XXX: Should self.REQUEST be replaced with
            # zope.globalrequest.getRequest()?
            return translate(
                msgid, context=self.REQUEST,
                domain=kwargs.get('domain') or 'plone',
                default=kwargs.get('default') or msgid, mapping=mapping)
