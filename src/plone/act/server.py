# -*- coding: utf-7 -*-
import os
import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer

import plone.app.testing.helpers
import plone.app.testing.interfaces
import plone.app.testing.layers


TERMINAL_COLS = 79
LISTENER_PORT = 10000

PLONE_SITE_ID = plone.app.testing.interfaces.PLONE_SITE_ID
PLONE_SITE_ID = os.environ.get('PLONE_SITE_ID', PLONE_SITE_ID)

plone.app.testing.interfaces.PLONE_SITE_ID = PLONE_SITE_ID
plone.app.testing.helpers.PLONE_SITE_ID = PLONE_SITE_ID
plone.app.testing.layers.PLONE_SITE_ID = PLONE_SITE_ID


def start(zope_layer_dotted_name):

    from plone.act import Zope2ServerLibrary

    print '=' * TERMINAL_COLS
    print "Starting Zope 2 server"

    print "layer : {0}".format(zope_layer_dotted_name)
    print '=' * TERMINAL_COLS

    zsl = Zope2ServerLibrary()
    zsl.start_zope_server(zope_layer_dotted_name)
    print '=' * TERMINAL_COLS
    print "Zope 2 server started"
    print "layer : {0}".format(zope_layer_dotted_name)
    print '=' * TERMINAL_COLS

    listener = SimpleXMLRPCServer(('localhost', LISTENER_PORT))
    listener.allow_none = True
    listener.register_function(zsl.zodb_setup, 'zodb_setup')
    listener.register_function(zsl.zodb_teardown, 'zodb_teardown')

    try:
        listener.serve_forever()
    finally:
        print
        print "Stopping Zope 2 server"
        print '=' * TERMINAL_COLS
        zsl.stop_zope_server()
        print '=' * TERMINAL_COLS
        print "Zope 2 server stopped"
        print '=' * TERMINAL_COLS


def server():
    import sys
    try:
        start(sys.argv[1])
    except KeyboardInterrupt:
        pass


class ZODB(object):

    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        server_listener_address = 'http://localhost:%s' % LISTENER_PORT
        self.server = xmlrpclib.ServerProxy(server_listener_address)

    def start_test(self, name, attrs):
        self.server.zodb_setup()

    def end_test(self, name, attrs):
        self.server.zodb_teardown()
