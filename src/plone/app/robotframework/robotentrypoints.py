# -*- coding: utf-8 -*-
import sys

from robot import run_cli
from robot import rebot_cli


def robot():
    run_cli(['--listener', 'plone.app.robotframework.RobotListener']
            + sys.argv[1:])


def pybot():
    run_cli(sys.argv[1:])


def rebot():
    rebot_cli(sys.argv[1:])
