*** Settings ***

Documentation  This library requires
...            plone.app.robotframework.testing.SPEAKJS_FIXTURE

Library  String

*** Keywords ***

Speak
    [Documentation]  Speaks out the given test using speak.js (in english).
    [Arguments]   ${text}
    ${escaped} =  Replace string  ${text}  '   \\'
    Execute Javascript
    ...    return (function(){
    ...        if (jq('#audio').length == 0) {
    ...            jq('<div id="audio"></div>').appendTo($('body'));
    ...        }
    ...        speak('${escaped}');
    ...        return true;
    ...    })();
