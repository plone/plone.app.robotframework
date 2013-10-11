*** Settings ***

Variables  plone/app/testing/interfaces.py
Variables  plone/app/robotframework/variables.py

*** Variables ***

${ZOPE_URL}  http://${ZOPE_HOST}:${ZOPE_PORT}

${PLONE_SITE_ID}  plone
${PLONE_URL}  ${ZOPE_URL}/${PLONE_SITE_ID}

${START_URL}  ${PLONE_URL}
