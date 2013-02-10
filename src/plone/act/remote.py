# -*- coding: utf-8 -*-
from OFS.SimpleItem import SimpleItem


class RemoteKeywordsLibrary(SimpleItem):
    """Robot Framework Remote Library Tool for Plone

    See also: http://robotframework.googlecode.com/hg/doc/userguide/RobotFrameworkUserGuide.html?r=2.7.65#remote-library-interface

    """

    def __init__(self, keywords=None):
        self.keywords = keywords

    def get_keyword_names(self):
        """Return names of the implemented keywords
        """
        names = filter(lambda x: x[0] != '_', dir(self.keywords))
        return names

    def run_keyword(self, name, args):
        """Execute the specified keyword with given arguments.
        """
        func = getattr(self.keywords, name, None)
        result = {'error': '', 'return': ''}
        try:
            retval = func(*args)
        except Exception, e:
            result['status'] = 'FAIL'
            result['error'] = str(e)
        else:
            result['status'] = 'PASS'
            result['return'] = retval
        return result
