*** Settings ***

Documentation  This file should be required only using
...            ``Resource  plone/app/robotframework/variables.robot``.
...
...            The fancy import order is required for backwards
...            compatibility with robotframework 2.7.7.

*** Variables ***

${ZOPE_URL}  http://${ZOPE_HOST}:${ZOPE_PORT}

${PLONE_SITE_ID}  plone
${PLONE_URL}  ${ZOPE_URL}/${PLONE_SITE_ID}

${START_URL}  ${PLONE_URL}
