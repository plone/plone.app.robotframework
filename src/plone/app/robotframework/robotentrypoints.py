# -*- coding: utf-8 -*-
import sys

from robot import run_cli

import pkg_resources

try:
    pkg_resources.get_distribution('robotframework-ride')
except pkg_resources.DistributionNotFound:
    HAS_RIDE = False
else:
    HAS_RIDE = True


def pybot():
    run_cli(sys.argv[1:])


def robot():
    run_cli(['--listener', 'plone.app.robotframework.RobotListener']
            + sys.argv[1:])


def ride():
    if HAS_RIDE:
        from robotide import main
        main(*sys.argv[1:])
    else:
        print u"""\
Package robotframework-ride was not found. Please, install
plone.app.robotframework with proper extras, like:

    plone.app.robotframework[ride]

or

    plone.app.robotframework[ride,reload]

Remember that ride must be lauched with system python with
wxPython installed, like:

    /usr/bin/python bin/ride
"""
