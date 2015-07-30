from Products.CMFCore.utils import getToolByName
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.robotframework.testing import \
    PLONE_ROBOT_INTEGRATION_TESTING

import unittest


class TestCreateContent(unittest.TestCase):

    layer = PLONE_ROBOT_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def create_content(self, *args, **kwargs):
        from plone.app.robotframework.content import Content
        Content().create_content(*args, **kwargs)

    def test_create_content_without_id(self):
        self.create_content(
            type='Document',
            title='Document 1'
        )
        self.assertTrue('document-1' in self.portal.objectIds())

    def test_create_content(self):
        self.create_content(
            type='Document',
            id='doc1',
            title='Document 1'
        )
        self.assertTrue('doc1' in self.portal.objectIds())

    def test_create_image(self):
        self.create_content(
            type='Image',
            id='image1',
            title='Image 1'
        )
        self.assertTrue('image1' in self.portal.objectIds())

    def test_create_news(self):
        self.create_content(
            type='News Item',
            id='news1',
            title='News 1'
        )
        self.assertTrue('news1' in self.portal.objectIds())

    def test_create_content_requires_type(self):
        self.assertRaises(
            AssertionError,
            self.create_content,
            id='d',
        )

    def test_create_content_updates_catalog(self):
        self.create_content(
            type='Document',
            id='doc1',
            title='Document 1'
        )
        catalog = getToolByName(self.portal, "portal_catalog")
        self.assertEqual(len(catalog(portal_type="Document")), 1)


class TestGlobalAllow(unittest.TestCase):

    layer = PLONE_ROBOT_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.types_tool = getToolByName(self.portal, "portal_types")
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def global_allow(self, *args, **kwargs):
        from plone.app.robotframework.content import Content
        Content().global_allow(*args, **kwargs)

    def test_global_allow(self):
        self.types_tool['Document'].global_allow = False
        self.assertRaises(
            ValueError,
            self.portal.invokeFactory,
            'Document', 'doc1',
        )

        self.global_allow('Document')
        self.portal.invokeFactory('Document', 'doc1')

        self.assertTrue('doc1' in self.portal.objectIds())
