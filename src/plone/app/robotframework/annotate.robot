*** Settings ***

Documentation  This library expects jQuery to be found from the tested page.

Library  String
Library  Collections
Library  plone.app.robotframework.Annotate

*** Variables ***

${CROP_MARGIN} =  10

*** Keywords ***

Normalize annotation locator
    [Arguments]  ${locator}
    ${locator} =  Replace string  ${locator}  '  \\'
    ${locator} =  Replace string using regexp  ${locator}  ^jquery=  ${empty}
    ${locator} =  Replace string using regexp  ${locator}  ^css=  ${empty}
    [return]  ${locator}

Add dot
    [Arguments]  ${locator}  ${display}=block
    ${selector} =  Normalize annotation locator  ${locator}
    ${display} =  Replace string  ${display}  '  \\'
    ${id} =  Execute Javascript
    ...    return (function(){
    ...        var id = 'id' + Math.random().toString().substring(2);
    ...        var annotation = jQuery('<div></div>');
    ...        var target = jQuery('${selector}');
    ...        var offset = target.offset();
    ...        var height = target.outerHeight();
    ...        var width = target.outerWidth();
    ...        annotation.attr('id', id);
    ...        annotation.css({
    ...            'display': '${display}',
    ...            'opacity': '0.5',
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
    ...        jQuery('body').append(annotation);
    ...        return id;
    ...    })();
    [return]  ${id}


Add note
    [Arguments]  ${locator}  ${message}
    ...          ${background}=#fcf0ad
    ...          ${color}=black
    ...          ${border}=none
    ...          ${display}=block
    ${selector} =  Normalize annotation locator  ${locator}
    ${message} =  Replace string  ${message}  '  \\'
    ${background} =  Replace string  ${background}  '  \\'
    ${color} =  Replace string  ${color}  '  \\'
    ${border} =  Replace string  ${border}  '  \\'
    ${display} =  Replace string  ${display}  '  \\'
    ${id} =  Execute Javascript
    ...    return (function(){
    ...        var id = 'id' + Math.random().toString().substring(2);
    ...        var annotation = jQuery('<div></div>');
    ...        var target = jQuery('${selector}');
    ...        var offset = target.offset();
    ...        var width = target.outerWidth();
    ...        var height = target.outerHeight();
    ...        annotation.attr('id', id);
    ...        annotation.text('${message}');
    ...        annotation.css({
    ...            'display': '${display}',
    ...            'position': 'absolute',
    ...            'font-family': 'serif',
    ...            'box-shadow': '0 0 5px #888',
    ...            '-moz-box-sizing': 'border-box',
    ...            '-webkit-box-sizing': 'border-box',
    ...            'box-sizing': 'border-box',
    ...            'padding': '0.5ex 0.5em',
    ...            'border': '${border}',
    ...            'border-radius': '2px',
    ...            'background': '${background}',
    ...            'color': '${color}',
    ...            'z-index': '9999',
    ...            'width': '140px',
    ...            'top': (offset.top + height / 2).toString() + 'px',
    ...            'left': (offset.left + width / 2 - 70).toString() + 'px',
    ...        });
    ...        jQuery('body').append(annotation);
    ...        return id;
    ...    })();
    [return]  ${id}

Remove element
    [Arguments]  ${id}
    Execute Javascript
    ...    return (function(){
    ...        jQuery('#${id}').remove();
    ...        return true;
    ...    })();

Update element style
    [Arguments]  ${id}  ${name}  ${value}
    ${name} =  Replace string  ${name}  '  \\'
    ${value} =  Replace string  ${value}  '  \\'
    Execute Javascript
    ...    return (function(){
    ...        jQuery('#${id}').css({
    ...            '${name}': '${value}'
    ...        });
    ...        return true;
    ...    })();
    [return]  ${id}

Crop page screenshot
    [Arguments]  ${filename}  @{locators}
    @{selectors} =  Create list
    :FOR  ${locator}  IN  @{locators}
    \  ${selector} =  Normalize annotation locator  ${locator}
    \  Append to list  ${selectors}  ${selector}
    ${selectors} =  Convert to string  ${selectors}
    ${selectors} =  Replace string using regexp  ${selectors}  u'  '
    @{dimensions} =  Execute Javascript
    ...    return (function(){
    ...        var selectors = ${selectors}, i, target, offset;
    ...        var left = null, top = null, width = null, height = null;
    ...        for (i = 0; i < selectors.length; i++) {
    ...            target = jQuery(selectors[i]);
    ...            offset = target.offset();
    ...            if (left === null) { left = offset.left; }
    ...            else { left = Math.min(left, offset.left); }
    ...            if (top === null) { top = offset.top; }
    ...            else { top = Math.min(top, offset.top); }
    ...            if (width === null) { width = target.outerWidth(); }
    ...            else {
    ...                width = Math.max(
    ...                    left + width, offset.left + target.outerWidth()
    ...                ) - left;
    ...             }
    ...            if (height === null) { height = target.outerHeight(); }
    ...            else {
    ...                height = Math.max(
    ...                    top + height, offset.top + target.outerHeight()
    ...                ) - top;
    ...            }
    ...        }
    ...        return [left - ${CROP_MARGIN},
    ...                top - ${CROP_MARGIN},
    ...                width + ${CROP_MARGIN} * 2,
    ...                height + ${CROP_MARGIN} * 2];
    ...    })();
    Crop image  ${OUTPUT_DIR}  ${filename}  @{dimensions}
