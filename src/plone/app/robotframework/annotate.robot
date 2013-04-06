*** Settings ***
Documentation  This library expects jQuery to be found from the page to be
...            tested.

Library  Dialogs

*** Keywords ***

Add dot
    [Arguments]  ${jqlocator}
    ${id} =  Execute Javascript
    ...    return (function(){
    ...        var id = 'id' + Math.random().toString().substring(2);
    ...        var annotation = jq('<div></div>');
    ...        var target = jq("${jqlocator}");
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
    [Arguments]  ${jqlocator}  ${sleep}  ${message}
    ...          ${background}=white
    ...          ${color}=black
    ...          ${border}=1px solid black
    ${id} =  Execute Javascript
    ...    return (function(){
    ...        var id = 'id' + Math.random().toString().substring(2);
    ...        var annotation = jq('<div></div>');
    ...        var target = jq("${jqlocator}");
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
    [Arguments]  ${jqlocator}  ${sleep}  ${message}
    ...          ${background}=white
    ...          ${color}=black
    ...          ${border}=1px solid black
    ${dot-id} =  Add dot  ${jqlocator}
    Sleep  1s
    Speak  ${message}
    ${note-id} =  Add note  ${jqlocator}  ${sleep}  ${message}
    ...                     ${background}  ${color}  ${border}
    Sleep  2s
    Remove element by id  ${dot-id}
    Remove element by id  ${note-id}

Speak
    [Arguments]   ${text}
    Execute Javascript
    ...    return (function(){
    ...        if (jq('#audio').length == 0) {
    ...            jq('<div id="audio"></div>').appendTo($('body'));
    ...        }
    ...        speak("${text}");
    ...        return true;
    ...    })();


