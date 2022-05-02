from OFS.SimpleItem import SimpleItem
from plone.app.testing import PLONE_FIXTURE
from plone.testing import Layer
from Products.CMFPlone.Portal import PloneSite


class RemoteLibrary(SimpleItem):
    """Robot Framework remote library base for Plone

    http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#remote-library-interface
    https://github.com/robotframework/PythonRemoteServer/blob/master/src/robotremoteserver.py
    """

    def get_keyword_names(self):
        """Return names of the implemented keywords"""
        blacklist = dir(SimpleItem)
        blacklist.extend(
            [
                "get_keyword_names",
                "get_keyword_arguments",
                "get_keyword_documentation",
                "run_keyword",
            ]
        )
        names = [x for x in dir(self) if x[0] != "_" and x not in blacklist]
        return names

    def get_keyword_arguments(self, name):
        """Return keyword arguments"""
        return None

    def get_keyword_documentation(self, name):
        """Return keyword documentation"""
        func = getattr(self, name, None)
        return func.__doc__ if func else ""

    def run_keyword(self, name, args, kwargs={}):
        """Execute the specified keyword with given arguments."""
        func = getattr(self, name, None)
        result = {"error": "", "return": ""}
        try:
            retval = func(*args, **kwargs)
        except Exception as e:
            result["status"] = "FAIL"
            result["error"] = str(e)
        else:
            result["status"] = "PASS"
            result["return"] = retval
            result["output"] = retval
        return result


class RemoteLibraryLayer(Layer):

    defaultBases = (PLONE_FIXTURE,)
    libraryBases = ()

    def __init__(self, *args, **kwargs):
        kwargs["name"] = kwargs.get("name", "RobotRemote")
        self.libraryBases = (RemoteLibrary,) + kwargs.pop("libraries", ())
        super().__init__(*args, **kwargs)

    def setUp(self):
        id_ = self.__name__.split(":")[-1]
        assert id_ not in globals(), "Conflicting remote library id: %s" % id_
        globals()[id_] = Remote = type(id_, self.libraryBases, {})
        setattr(PloneSite, id_, Remote())

    def tearDown(self):
        id_ = self.__name__.split(":")[-1]
        delattr(PloneSite, id_)
        del globals()[id_]
