# -*- coding: utf-8 -*-
import os

from Products.CMFCore.utils import getToolByName
from plone.app.robotframework.remote import RemoteLibrary
from plone.app.robotframework.utils import disableCSRFProtection
from zope.component.hooks import getSite
from zope.globalrequest import getRequest
from zope.i18n import translate


class I18N(RemoteLibrary):

    def set_default_language(self, language=None):
        """Change portal default language"""
        disableCSRFProtection()
        portal = getSite()
        portal_languages = getToolByName(portal, 'portal_languages')
        if language is None:
            language = os.environ.get('LANGUAGE') or 'en'
        setattr(portal, 'language', language)
        portal_languages.setDefaultLanguage(language)

    def translate(self, msgid, *args, **kwargs):
        """Return localized string for given msgid"""
        # XXX: Because kwargs are only supported with robotframework >= 2.8.3,
        # we must parse them here to support robotframework < 2.8.3.
        for arg in [x for x in args if '=' in x]:
            name, value = arg.split('=', 1)
            kwargs[name] = value

        mapping = {}
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
            request = getRequest()
            return translate(
                msgid, context=request,
                domain=kwargs.get('domain') or 'plone',
                default=kwargs.get('default') or msgid, mapping=mapping)