# -*- coding: utf-8 -*-

# WARNING: This module must not be imported outside running babel

MESSAGES = []

def populate(self):
    if self._value or self._comments:
        self._setter(self._value, self._comments.value)
    try:
        parts = map(unicode.lower, self._value)
        index = parts.index('translate')
        comments = []
        for part in filter(lambda x: x.startswith('default='), self._value):
            comments.append('Default: "%s"' % part[8:])
        MESSAGES.append((0, None, self._value[index + 1], comments))
    except ValueError:
        pass
    except IndexError:
        pass

import robot.parsing.tablepopulators
robot.parsing.tablepopulators.StepPopulator.populate = populate

import robot


def extract_robot(fileobj, keywords, comment_tags, options):
    global MESSAGES
    try:
        robot.parsing.TestData(source=fileobj.name)
    except robot.errors.DataError:
        pass
    while MESSAGES:
        yield MESSAGES.pop()
