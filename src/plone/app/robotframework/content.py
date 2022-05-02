from datetime import datetime
from io import BytesIO
from PIL import Image
from PIL import ImageDraw
from plone.app.robotframework.remote import RemoteLibrary
from plone.app.robotframework.utils import disableCSRFProtection
from plone.app.textfield.value import RichTextValue
from plone.dexterity.utils import getAdditionalSchemata
from plone.namedfile.file import NamedBlobFile
from plone.namedfile.file import NamedBlobImage
from plone.uuid.interfaces import IUUID
from Products.CMFCore.utils import getToolByName
from z3c.form.interfaces import IDataConverter
from z3c.form.interfaces import IDataManager
from z3c.form.interfaces import IFieldWidget
from zope.component import ComponentLookupError
from zope.component import getUtility
from zope.component import queryMultiAdapter
from zope.component.hooks import getSite
from zope.event import notify
from zope.globalrequest import getRequest
from zope.lifecycleevent import ObjectModifiedEvent
from zope.schema.interfaces import IFromUnicode

import os
import pkg_resources
import random
import string


try:
    pkg_resources.get_distribution("z3c.relationfield")
except pkg_resources.DistributionNotFound:
    HAS_DEXTERITY_RELATIONS = False
else:
    from z3c.relationfield import RelationValue
    from zope.intid.interfaces import IIntIds

    HAS_DEXTERITY_RELATIONS = True


class Content(RemoteLibrary):
    def delete_content(self, uid_or_path):
        """Delete content by uid or path"""
        disableCSRFProtection()
        portal = getSite()
        pc = getToolByName(portal, "portal_catalog")
        uid_results = pc.unrestrictedSearchResults(UID=uid_or_path)
        path_results = pc.unrestrictedSearchResults(
            path={"query": uid_or_path.rstrip("/"), "depth": 0}
        )
        content = (uid_results or path_results)[0]._unrestrictedGetObject()
        content.aq_parent.manage_delObjects([content.getId()])

    def create_content(self, *args, **kwargs):
        """Create content and return its UID"""
        disableCSRFProtection()
        # XXX: Because kwargs are only supported with robotframework >= 2.8.3,
        # we must parse them here to support robotframework < 2.8.3.
        for arg in [x for x in args if "=" in x]:
            name, value = arg.split("=", 1)
            kwargs[name] = value

        assert "type" in kwargs, "Keyword arguments must include 'type'."
        portal_type = kwargs.get("type")
        portal = getSite()
        if "container" in kwargs:
            pc = getToolByName(portal, "portal_catalog")
            uid_or_path = kwargs.pop("container")
            uid_results = pc.unrestrictedSearchResults(UID=uid_or_path)
            path_results = pc.unrestrictedSearchResults(
                path={"query": uid_or_path.rstrip("/"), "depth": 0}
            )
            container = (uid_results or path_results)[0]._unrestrictedGetObject()
        else:
            container = portal

        # if we create 'file' and 'image' kwargs entries, they should not be
        # used to create the content but be set afterwards
        create_kwargs = {}
        create_kwargs.update(kwargs)

        if portal_type in ("File",) and "file" not in kwargs:
            pdf_file = os.path.join(os.path.dirname(__file__), "content", "file.pdf")
            with open(pdf_file, "rb") as f:
                file_data = f.read()
            value = NamedBlobFile(
                data=file_data, contentType="application/pdf", filename="file.pdf"
            )
            kwargs["file"] = value

        if portal_type in ("Image", "News Item") and "image" not in kwargs:
            prefill_image_types(kwargs)

        id_ = kwargs.pop("id", None)
        type_ = kwargs.pop("type")

        content = None
        # The title attribute needs to be unicode.
        if "title" in kwargs and isinstance(kwargs["title"], bytes):
            kwargs["title"] = kwargs["title"].decode("utf-8")
            create_kwargs["title"] = create_kwargs["title"].decode("utf-8")
        from plone.dexterity.interfaces import IDexterityFTI
        from plone.dexterity.utils import createContentInContainer

        try:
            getUtility(IDexterityFTI, name=type_)
            content = createContentInContainer(container, type_, **create_kwargs)
            if id_ is not None and content.id != id_:
                container.manage_renameObject(content.id, id_)
        except ComponentLookupError:
            pass

        if content:
            # We need a second pass to fill all fields using their widgets to
            # get e.g. RichText-values created correctly.
            fti = getUtility(IDexterityFTI, name=type_)
            schema = fti.lookupSchema()
            fields = {}
            for name in schema:
                fields[name] = schema[name]
            for schema in getAdditionalSchemata(portal_type=type_):
                for name in schema:
                    fields[name] = schema[name]
            for name, field in fields.items():
                widget = queryMultiAdapter((field, getRequest()), IFieldWidget)
                if widget and name in kwargs:
                    if not IFromUnicode.providedBy(field):
                        value = kwargs[name]
                    elif isinstance(kwargs[name], str):
                        value = kwargs[name]
                    else:
                        value = str(str(kwargs[name]), "utf-8", errors="ignore")
                    converter = IDataConverter(widget)
                    dm = queryMultiAdapter((content, field), IDataManager)
                    if dm:
                        dm.set(converter.toFieldValue(value))

        return IUUID(content)

    def set_field_value(self, uid, field, value, field_type):
        """Set field value with a specific type"""
        pc = getToolByName(self, "portal_catalog")
        results = pc.unrestrictedSearchResults(UID=uid)
        obj = results[0]._unrestrictedGetObject()
        if field_type == "float":
            value = float(value)
        if field_type == "int":
            value = int(value)
        if field_type == "list":
            value = eval(value)
        if field_type.startswith("datetime"):
            # field_type must begin with 'datetime'
            # followed by optional format 'datetime%Y%m%d%H%M'
            # without format: %Y%m%d%H%M is used
            field_type = field_type[8:]
            fmt = field_type and field_type or "%Y%m%d%H%M"
            value = datetime.strptime(value, fmt)
        if field_type.startswith("date"):
            # field_type must begin with 'date'
            # followed by optional format 'date%Y%m%d'
            # without format: %Y%m%d is used
            field_type = field_type[4:]
            fmt = field_type and field_type or "%Y%m%d"
            value = datetime.strptime(value, fmt).date()
        if field_type == "reference" and HAS_DEXTERITY_RELATIONS:
            results_referenced = pc.unrestrictedSearchResults(UID=value)
            referenced_obj = results_referenced[0]._unrestrictedGetObject()
            intids = getUtility(IIntIds)
            referenced_obj_intid = intids.getId(referenced_obj)
            value = RelationValue(referenced_obj_intid)
        if field_type == "references" and HAS_DEXTERITY_RELATIONS:
            values = eval(value)
            intids = getUtility(IIntIds)
            value = []
            for uid in values:
                results_referenced = pc.unrestrictedSearchResults(UID=uid)
                referenced_obj = results_referenced[0]._unrestrictedGetObject()
                referenced_obj_intid = intids.getId(referenced_obj)
                value.append(RelationValue(referenced_obj_intid))
        if field_type == "text/html":
            value = RichTextValue(value, "text/html", "text/html")
            obj.text = value
        if field_type == "file":
            pdf_file = os.path.join(os.path.dirname(__file__), "content", "file.pdf")
            with open(pdf_file, "rb") as f:
                file_data = f.read()
            value = NamedBlobFile(
                data=file_data, contentType="application/pdf", filename="file.pdf"
            )
        if field_type == "image":
            image_file = os.path.join(os.path.dirname(__file__), "image.jpg")
            with open(image_file, "rb") as f:
                image_data = f.read()
            value = NamedBlobImage(
                data=image_data, contentType="image/jpg", filename="image.jpg"
            )

        setattr(obj, field, value)
        obj.reindexObject()
        notify(ObjectModifiedEvent(obj))

    def uid_to_url(self, uid):
        """Return absolute path for an UID"""
        pc = getToolByName(self, "portal_catalog")
        results = pc.unrestrictedSearchResults(UID=str(uid))
        if not results:
            return None
        else:
            return results[0].getURL()

    def path_to_uid(self, path):
        """Return UID for an absolute path"""
        pc = getToolByName(self, "portal_catalog")
        results = pc.unrestrictedSearchResults(
            path={"query": path.rstrip("/"), "depth": 0}
        )
        if not results:
            return None
        else:
            return results[0].UID

    def fire_transition(self, content, action):
        """Fire workflow action for content"""
        disableCSRFProtection()
        # It should be ok to use unrestricted-methods, because workflow
        # transition guard should proctect unprivileged transition:
        pc = getToolByName(self, "portal_catalog")
        results = pc.unrestrictedSearchResults(UID=content)
        obj = results[0]._unrestrictedGetObject()
        wftool = getToolByName(obj, "portal_workflow")
        wftool.doActionFor(obj, action)

    do_action_for = fire_transition

    def global_allow(self, type_, value=True):
        """Allow type to be added globally."""
        disableCSRFProtection()
        portal = getSite()
        types_tool = getToolByName(portal, "portal_types")
        types_tool[type_].global_allow = value


def prefill_image_types(kwargs):
    image = random_image()
    filename = "{}.png".format(
        "".join(random.choice(string.ascii_lowercase) for _ in range(6))
    )
    kwargs["image"] = NamedBlobImage(data=image, filename=filename)


def random_image():
    img = Image.new("RGB", (random.randint(320, 640), random.randint(320, 640)))
    draw = ImageDraw.Draw(img)
    draw.rectangle(
        ((0, 0), img.size),
        fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
    )
    del draw

    result = BytesIO()
    img.save(result, "PNG")
    result.seek(0)
    return result.read()
