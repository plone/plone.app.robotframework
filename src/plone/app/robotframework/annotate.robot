*** Settings ***
Documentation  This library expects jQuery to be found from the page to be
...            tested.

Library  String

Resource  speak.robot


*** Keywords ***

Add dot
    [Arguments]  ${locator}
    ${selector} =  Replace string using regexp  ${locator}  ^css=  ${empty}
    ${id} =  Execute Javascript
    ...    return (function(){
    ...        var id = 'id' + Math.random().toString().substring(2);
    ...        var annotation = jq('<div></div>');
    ...        var target = jq("${selector}");
    ...        var offset = target.offset();
    ...        var height = target.height();
    ...        var width = target.width();
    ...        annotation.attr('id', id);
    ...        annotation.css({
    ...            'position': 'absolute',
    ...            'background': 'black',
    ...            'color': 'white',
    ...            'border-radius': '10px',
    ...            'width': '20px',
    ...            'height': '20px',
    ...            'top': (offset.top + height / 2 - 10).toString() + 'px',
    ...            'left': (offset.left + width / 2 - 10).toString() + 'px',
    ...            'z-index': '9999',
    ...        });
    ...        jq('body').append(annotation);
    ...        return id;
    ...    })();
    [return]  ${id}

Add note
    [Arguments]  ${locator}  ${sleep}  ${message}
    ...          ${background}=white
    ...          ${color}=black
    ...          ${border}=1px solid black
    ${selector} =  Replace string using regexp  ${locator}  ^css=  ${empty}
    ${id} =  Execute Javascript
    ...    return (function(){
    ...        var id = 'id' + Math.random().toString().substring(2);
    ...        var annotation = jq('<div></div>');
    ...        var target = jq("${selector}");
    ...        var offset = target.offset();
    ...        var height = target.height();
    ...        var width = target.width();
    ...        annotation.attr('id', id);
    ...        annotation.text("${message}");
    ...        annotation.css({
    ...            'position': 'absolute',
    ...            'padding': '1em',
    ...            'border-radius': '1ex',
    ...            'border': "${border}",
    ...            'background': "${background}",
    ...            'color': "${color}",
    ...            'z-index': '9999',
    ...            'width': '100px',
    ...            'top': (offset.top + height / 2).toString() + 'px',
    ...            'left': (offset.left + width / 2 - 50).toString() + 'px',
    ...        });
    ...        jq('body').append(annotation);
    ...        return id;
    ...    })();
    [return]  ${id}

Remove element by id
    [Arguments]  ${id}
    Execute Javascript
    ...    return (function(){
    ...        jq("#${id}").remove();
    ...        return true;
    ...    })();

Show note with dot
    [Arguments]  ${locator}  ${sleep}  ${message}
    ...          ${background}=white
    ...          ${color}=black
    ...          ${border}=1px solid black
    ${dot-id} =  Add dot  ${locator}
    Sleep  1s
    Speak  ${message}
    ${note-id} =  Add note  ${locator}  ${sleep}  ${message}
    ...                     ${background}  ${color}  ${border}
    Sleep  2s
    Remove element by id  ${dot-id}
    Remove element by id  ${note-id}
