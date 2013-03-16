import sys
import zope.deprecation
import plone.app.robotframework
sys.modules['plone.act'] = zope.deprecation.deprecation.deprecated(
    plone.app.robotframework,
    'A module called plone.act is now plone.app.robotframework.'
)
