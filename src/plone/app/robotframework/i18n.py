# -*- coding: utf-8 -*-
from plone.app.robotframework.remote import RemoteLibrary
from plone.app.robotframework.utils import disableCSRFProtection
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.globalrequest import getRequest
from zope.i18n import translate

import os


try:
    from plone.i18n.interfaces import ILanguageSchema
except ImportError:
    # BBB for Plone 5.1, remove with Plone 6
    from Products.CMFPlone.interfaces import ILanguageSchema


class I18N(RemoteLibrary):

    def set_default_language(self, language=None):
        """Change portal default language"""
        disableCSRFProtection()
        if language is None:
            language = os.environ.get('LANGUAGE') or 'en'
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ILanguageSchema, prefix='plone')
        settings.default_language = language

    def translate(self, msgid, *args, **kwargs):
        """Return localized string for given msgid"""
        # FIXME: we are alrady using robotframework = 3.0
        # XXX: Because kwargs are only supported with robotframework >= 2.8.3,
        # we must parse them here to support robotframework < 2.8.3.
        for arg in [x for x in args if '=' in x]:
            name, value = arg.split('=', 1)
            kwargs[name] = value

        mapping = {}
        for key, value in kwargs.items():
            if key not in ('target_language', 'domain', 'default'):
                mapping[key] = value
        if kwargs.get('target_language'):
            return translate(
                msgid,
                target_langauge=kwargs.get('target_language'),
                domain=kwargs.get('domain') or 'plone',
                default=kwargs.get('default') or msgid, mapping=mapping
            )
        else:
            # XXX: Should self.REQUEST be replaced with
            # zope.globalrequest.getRequest()?
            request = getRequest()
            return translate(
                msgid, context=request,
                domain=kwargs.get('domain') or 'plone',
                default=kwargs.get('default') or msgid, mapping=mapping
            )
