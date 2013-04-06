*** Settings ***

Variables  plone/app/testing/interfaces.py

*** Variables ***

${ZOPE_HOST}  localhost
${ZOPE_PORT}  55001
${ZOPE_URL}  http://${ZOPE_HOST}:${ZOPE_PORT}

${PLONE_SITE_ID}  plone
${PLONE_URL}  ${ZOPE_URL}/${PLONE_SITE_ID}

${START_URL}  ${PLONE_URL}
