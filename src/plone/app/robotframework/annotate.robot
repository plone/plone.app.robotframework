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
    [Arguments]  ${locator}  ${size}=20  ${display}=block
    ${selector} =  Normalize annotation locator  ${locator}
    ${size} =  Replace string  ${size}  '  \\'
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
    ...            'font-family': 'serif',
    ...            'text-align': 'center',
    ...            'opacity': '0.5',
    ...            '-moz-box-sizing': 'border-box',
    ...            '-webkit-box-sizing': 'border-box',
    ...            'box-sizing': 'border-box',
    ...            'position': 'absolute',
    ...            'color': 'white',
    ...            'background': 'black',
    ...            'width': '${size}px',
    ...            'height': '${size}px',
    ...            'border-radius': (${size} / 2).toString() + 'px',
    ...            'top': (
    ...                offset.top + height / 2 - ${size} / 2
    ...            ).toString() + 'px',
    ...            'left': (
    ...                offset.left + width / 2 - ${size} / 2
    ...            ).toString() + 'px',
    ...            'z-index': '9999'
    ...        });
    ...        jQuery('body').append(annotation);
    ...        return id;
    ...    })();
    [return]  ${id}

Add numbered dot
    [Arguments]  ${locator}  ${text}
    ...          ${background}=#fcf0ad
    ...          ${color}=black
    ...          ${display}=block
    ${id} =  Add dot  ${locator}  size=20  display=none
    Execute Javascript
    ...    return (function(){
    ...        jQuery('#${id}').css({
    ...            'opacity': '1',
    ...            'padding-top': '0.1em',
    ...            'box-shadow': '0 0 5px #888',
    ...            'background': '${background}',
    ...            'color': '${color}'
    ...        }).text('${text}');
    ...        return true;
    ...    })();
    Update element style  ${id}  display  ${display}
    [return]  ${id}

Add note
    [Arguments]  ${locator}  ${text}
    ...          ${background}=#fcf0ad
    ...          ${color}=black
    ...          ${border}=none
    ...          ${display}=block
    ...          ${width}=140
    ...          ${position}=${EMPTY}
    ${selector} =  Normalize annotation locator  ${locator}
    ${text} =  Replace string  ${text}  '  \\'
    ${background} =  Replace string  ${background}  '  \\'
    ${color} =  Replace string  ${color}  '  \\'
    ${border} =  Replace string  ${border}  '  \\'
    ${display} =  Replace string  ${display}  '  \\'
    ${width} =  Replace string  ${width}  '  \\'
    ${position} =  Replace string  ${position}  '  \\'
    ${id} =  Execute Javascript
    ...    return (function(){
    ...        var id = 'id' + Math.random().toString().substring(2);
    ...        var annotation = jQuery('<div></div>');
    ...        var target = jQuery('${selector}');
    ...        var offset = target.offset();
    ...        var width = target.outerWidth();
    ...        var height = target.outerHeight();
    ...        var maxLeft = jQuery('html').width()
    ...                      - ${width} - ${CROP_MARGIN};
    ...        annotation.attr('id', id);
    ...        annotation.text('${text}');
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
    ...            'width': '${width}px',
    ...            'top': Math.max(
    ...                 (offset.top + height / 2),
    ...                 ${CROP_MARGIN}
    ...            ).toString() + 'px',
    ...            'left': Math.max(${CROP_MARGIN}, Math.min(
    ...                 (offset.left + width / 2 - (${width} / 2)),
    ...                 maxLeft
    ...            )).toString() + 'px'
    ...        });
    ...        if ('${position}' === 'top') {
    ...            annotation.css({
    ...                'top': 'auto',
    ...                'bottom': (
    ...                    window.innerHeight - offset.top + ${CROP_MARGIN}
    ...                ).toString() + 'px'
    ...            });
    ...        } else if ('${position}' === 'bottom') {
    ...            annotation.css({
    ...                'top': (
    ...                    offset.top + height + ${CROP_MARGIN}
    ...                ).toString() + 'px'
    ...            });
    ...        } else if ('${position}' === 'left') {
    ...            annotation.css({
    ...                'left': (
    ...                    offset.left - ${width} - ${CROP_MARGIN} / 2
    ...                ).toString() + 'px'
    ...            });
    ...        } else if ('${position}' === 'right') {
    ...            annotation.css({
    ...                'left': (Math.min(
    ...                    offset.left + width + ${CROP_MARGIN} / 2,
    ...                    maxLeft
    ...                )).toString() + 'px'
    ...            });
    ...        }
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

Remove elements
    [Arguments]  @{ids}
    :FOR  ${id}  IN  @{ids}
    \  Remove element  ${id}

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

Capture and crop page screenshot
    [Arguments]  ${filename}  @{locators}
    Capture page screenshot  ${filename}
    Crop page screenshot  ${filename}  @{locators}
