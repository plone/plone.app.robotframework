# -*- coding: utf-8 -*-
from OFS.SimpleItem import SimpleItem
from plone.app.testing import (
    PLONE_FIXTURE,
    ploneSite
)
from plone.testing import Layer


class RemoteLibrary(SimpleItem):
    """Robot Framework remote library base for Plone

    http://robotframework.googlecode.com/hg/doc/userguide/RobotFrameworkUserGuide.html?r=2.7.7#remote-library-interface
    http://robotframework.googlecode.com/hg/tools/remoteserver/robotremoteserver.py

    """
    def get_keyword_names(self):
        """Return names of the implemented keywords
        """
        blacklist = dir(SimpleItem)
        blacklist.extend([
            'get_keyword_names',
            'get_keyword_arguments',
            'get_keyword_documentation',
            'run_keyword'
        ])
        names = filter(lambda x: x[0] != '_' and x not in blacklist, dir(self))
        return names

    def get_keyword_arguments(self, name):
        """Return keyword arguments
        """
        return None

    def get_keyword_documentation(self, name):
        """Return keyword documentation
        """
        func = getattr(self, name, None)
        return func.__doc__ if func else u''

    def run_keyword(self, name, args, kwargs={}):
        """Execute the specified keyword with given arguments.
        """
        func = getattr(self, name, None)
        result = {'error': '', 'return': ''}
        try:
            retval = func(*args, **kwargs)
        except Exception, e:
            result['status'] = 'FAIL'
            result['error'] = str(e)
        else:
            result['status'] = 'PASS'
            result['return'] = retval
            result['output'] = retval
        return result


class RemoteLibraryLayer(Layer):

    defaultBases = (PLONE_FIXTURE,)
    libraryBases = ()

    def __init__(self, *args, **kwargs):
        kwargs['name'] = kwargs.get('name', 'RobotRemote')
        self.libraryBases = (RemoteLibrary,) + kwargs.pop('libraries', ())
        super(RemoteLibraryLayer, self).__init__(*args, **kwargs)

    def setUp(self):
        id_ = self.__name__.split(':')[-1]
        assert id_ not in globals(), "Conflicting remote library id: %s" % id_
        globals()[id_] = type(id_, self.libraryBases, {})
        with ploneSite() as portal:
            portal._setObject(id_, globals()[id_]())

    def tearDown(self):
        id_ = self.__name__.split(':')[-1]
        with ploneSite() as portal:
            if id_ in portal.objectIds():
                portal._delObject(id_)
        del globals()[id_]
