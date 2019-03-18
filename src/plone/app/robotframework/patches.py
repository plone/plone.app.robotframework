# -*- coding: utf-8 -*-
# Patch selenium.is_connectable for Python 3.
# See https://github.com/SeleniumHQ/selenium/pull/6480
# and for Plone: https://github.com/plone/Products.CMFPlone/issues/2786
from selenium.webdriver.common import utils

try:
    # Python 3
    ConnectionResetError
except NameError:
    # Python 2
    ConnectionResetError = None


if ConnectionResetError is not None:
    orig_is_connectable = utils.is_connectable

    def patched_is_connectable(port, host="localhost"):
        try:
            return orig_is_connectable(port, host=host)
        except ConnectionResetError:
            # Try again once.
            return orig_is_connectable(port, host=host)

    utils.is_connectable = patched_is_connectable
