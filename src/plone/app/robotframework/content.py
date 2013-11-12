# -*- coding: utf-8 -*-
# GOOD
import pkg_resources
from zope.component.hooks import getSite

try:
    pkg_resources.get_distribution('plone.dexterity')
except pkg_resources.DistributionNotFound:
    HAS_DEXTERITY = False
else:
    HAS_DEXTERITY = True

from plone.uuid.interfaces import IUUID
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility, ComponentLookupError
from plone.app.robotframework.remote import RemoteLibrary


class Content(RemoteLibrary):

    def create_content(self, *args, **kwargs):
        """Create content and return its UID"""
        # XXX: It seems that **kwargs does not yet work with Robot Framework
        # remote library interface and that's why we need to unpack the
        # keyword arguments from positional args list.
        for arg in args:
            name, value = arg.split('=', 1)
            kwargs[name] = value
        assert 'id' in kwargs, u"Keyword arguments must include 'id'."
        assert 'type' in kwargs, u"Keyword arguments must include 'type'."
        if 'container' in kwargs:
            pc = getToolByName(self, 'portal_catalog')
            results = pc.unrestrictedSearchResults(UID=kwargs.pop('container'))
            container = results[0]._unrestrictedGetObject()
        else:
            container = getSite()

        # Pre-fill Image-types with random content
        if kwargs.get('type') == 'Image' and not 'image' in kwargs:
            import random
            import StringIO
            from PIL import (
                Image,
                ImageDraw
            )
            img = Image.new('RGB', (random.randint(320, 640),
                                    random.randint(320, 640)))
            draw = ImageDraw.Draw(img)
            draw.rectangle(((0, 0), img.size), fill=(random.randint(0, 255),
                                                     random.randint(0, 255),
                                                     random.randint(0, 255)))
            del draw

            kwargs['image'] = StringIO.StringIO()
            img.save(kwargs['image'], 'PNG')
            kwargs['image'].seek(0)

        id_ = kwargs.pop('id')
        type_ = kwargs.pop('type')

        content = None
        if HAS_DEXTERITY:
            from plone.dexterity.interfaces import IDexterityFTI
            from plone.dexterity.utils import createContentInContainer
            try:
                getUtility(IDexterityFTI, name=type_)
                content = createContentInContainer(container, type_, **kwargs)
                if content.id != id_:
                    container.manage_renameObject(content.id, id_)
            except ComponentLookupError:
                pass

        if content is None:
            # It must be Archetypes based content:
            content = container[container.invokeFactory(type_, id_, **kwargs)]
            content.processForm()

        return IUUID(content)

    def uid_to_url(self, uid):
        """Return absolute path for an UID"""
        pc = getToolByName(self, 'portal_catalog')
        results = pc.unrestrictedSearchResults(UID=str(uid))
        if not results:
            return None
        else:
            return results[0].getURL()

    def fire_transition(self, content, action):
        """Fire workflow action for content"""
        # It should be ok to use unrestricted-methods, because workflow
        # transition guard should proctect unprivileged transition:
        pc = getToolByName(self, 'portal_catalog')
        results = pc.unrestrictedSearchResults(UID=content)
        obj = results[0]._unrestrictedGetObject()
        wftool = getToolByName(obj, 'portal_workflow')
        wftool.doActionFor(obj, action)

    do_action_for = fire_transition
