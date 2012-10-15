from plone.testing import z2
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import FunctionalTesting

import plone.act

LIVESEARCH = PloneWithPackageLayer(zcml_package=plone.act,
        zcml_filename='profiles.zcml', gs_profile_id='plone.act:content',
        name="LIVESEARCH")

LIVESEARCH_ZSERVER = FunctionalTesting(bases=(LIVESEARCH, z2.ZSERVER_FIXTURE),
        name='LIVESEARCH_ZSERVER')
