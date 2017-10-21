import sys


PY3 = sys.version_info[0] == 3
if PY3:
    from http.client import HTTPConnection
    from io import StringIO
    from xmlrpc.client import ServerProxy
    from xmlrpc.server import SimpleXMLRPCServer
else:
    from httplib import HTTPConnection
    from StringIO import StringIO
    from xmlrpclib import ServerProxy
    from SimpleXMLRPCServer import SimpleXMLRPCServer
