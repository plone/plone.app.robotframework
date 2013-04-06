*** Settings ***

Documentation  This library expects jQuery to be found from the tested page.

Library  String

*** Keywords ***

Add dot
    [Arguments]  ${locator}  ${display}=block
    ${selector} =  Replace string  ${locator}  '  \\'
    ${selector} =  Replace string using regexp  ${selector}  ^jquery=  ${empty}
    ${display} =  Replace string  ${display}  '  \\'
    ${id} =  Execute Javascript
    ...    return (function(){
    ...        var id = 'id' + Math.random().toString().substring(2);
    ...        var annotation = jq('<div></div>');
    ...        var target = jq('${selector}');
    ...        var offset = target.offset();
    ...        var height = target.height();
    ...        var width = target.width();
    ...        annotation.attr('id', id);
    ...        annotation.css({
    ...            'display': '${display}',
    ...            '-moz-box-sizing': 'border-box',
    ...            '-webkit-box-sizing': 'border-box',
    ...            'box-sizing': 'border-box',
    ...            'position': 'absolute',
    ...            'color': 'white',
    ...            'background': 'black',
    ...            'width': '20px',
    ...            'height': '20px',
    ...            'border-radius': '10px',
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
    ...          ${display}=block
    ${selector} =  Replace string  ${locator}  '  \\'
    ${selector} =  Replace string using regexp  ${selector}  ^jquery=  ${empty}
    ${message} =  Replace string  ${message}  '  \\'
    ${background} =  Replace string  ${background}  '  \\'
    ${color} =  Replace string  ${color}  '  \\'
    ${border} =  Replace string  ${border}  '  \\'
    ${display} =  Replace string  ${display}  '  \\'
    ${id} =  Execute Javascript
    ...    return (function(){
    ...        var id = 'id' + Math.random().toString().substring(2);
    ...        var annotation = jq('<div></div>');
    ...        var target = jq('${selector}');
    ...        var offset = target.offset();
    ...        var height = target.height();
    ...        var width = target.width();
    ...        annotation.attr('id', id);
    ...        annotation.text('${message}');
    ...        annotation.css({
    ...            'display': '${display}',
    ...            'position': 'absolute',
    ...            '-moz-box-sizing': 'border-box',
    ...            '-webkit-box-sizing': 'border-box',
    ...            'box-sizing': 'border-box',
    ...            'padding': '0.5ex 0.5em',
    ...            'border-radius': '1ex',
    ...            'border': '${border}',
    ...            'background': '${background}',
    ...            'color': '${color}',
    ...            'z-index': '9999',
    ...            'width': '100px',
    ...            'top': (offset.top + height / 2).toString() + 'px',
    ...            'left': (offset.left + width / 2 - 50).toString() + 'px',
    ...        });
    ...        jq('body').append(annotation);
    ...        return id;
    ...    })();
    [return]  ${id}

Remove element
    [Arguments]  ${id}
    Execute Javascript
    ...    return (function(){
    ...        jq('#${id}').remove();
    ...        return true;
    ...    })();

Update element style
    [Arguments]  ${id}  ${name}  ${value}
    ${name} =  Replace string  ${name}  '  \\'
    ${value} =  Replace string  ${value}  '  \\'
    Execute Javascript
    ...    return (function(){
    ...        jq('#${id}').css({
    ...            '${name}': '${value}'
    ...        });
    ...        return true;
    ...    })();
    [return]  ${id}
