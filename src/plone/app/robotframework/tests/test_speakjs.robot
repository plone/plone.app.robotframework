*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/saucelabs.robot
Resource  plone/app/robotframework/annotate.robot

Test Setup  Open SauceLabs test browser
Test Teardown  Run keywords  Report test status  Close all browsers

*** Test cases ***

Say something
    Go to  ${PLONE_URL}
    Show note with dot  \#content  2s  Plone is content
    Show note with dot  \#portaltab-index_html  2s  Plone is home
    Show note with dot  \#portal-logo  2s  Plone is a logo
#   Show note with dot  \#portal-footer  2s  Plone is footer
#   Show note with dot  \#portal-siteactions  2s  Plone is actions
    Speak  Welcome to Plone
    Sleep  2s
    Speak  I am mister roboto
    Sleep  2s
    Speak  'asta la vistaa, baby
    Sleep  3s
