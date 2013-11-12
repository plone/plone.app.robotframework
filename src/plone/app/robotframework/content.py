# -*- coding: utf-8 -*-
from plone.uuid.interfaces import IUUID
from plone import api
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
            kwargs['container'] = api.content.get(UID=kwargs['container'])
        else:
            kwargs['container'] = api.portal.get()

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

        return IUUID(api.content.create(**kwargs))

    def fire_transition(self, content, action):
        """Fire workflow action for content"""
        # It should be ok to use unrestricted-methods, because workflow
        # transition guard should proctect unprivileged transition:
        obj = self.portal_catalog.unrestrictedSearchResults(
            UID=content)[0]._unrestrictedGetObject()
        api.content.transition(obj, action)
