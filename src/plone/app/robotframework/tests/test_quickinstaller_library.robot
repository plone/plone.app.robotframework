*** Settings ***

Resource  plone/app/robotframework/variables.robot

Library  Remote  ${PLONE_URL}/RobotRemote

*** Test Cases ***

Some default product is activated
    Given 'plone.app.users' is activated
      and 'plone.session' is not activated

*** Keywords ***

'${product}' is activated
    Product is activated  ${product}

'${product}' is not activated
    Run keyword and expect error  *  Product is activated  ${product}
