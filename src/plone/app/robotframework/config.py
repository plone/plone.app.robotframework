# -*- coding: utf-8 -*-

import pkg_resources

try:
    pkg_resources.get_distribution('plone.dexterity')
except pkg_resources.DistributionNotFound:
    HAS_DEXTERITY = False
else:
    HAS_DEXTERITY = True


try:
    pkg_resources.get_distribution('z3c.relationfield')
except pkg_resources.DistributionNotFound:
    HAS_DEXTERITY_RELATIONS = False
else:
    HAS_DEXTERITY_RELATIONS = True
