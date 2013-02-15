# -*- coding: utf-8 -*-
import sys
import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer


TERMINAL_COLS = 79
LISTENER_PORT = 10000


def start(zope_layer_dotted_name):

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


class Zope2ServerLibrary(object):

    def __init__(self):
        self.zope_layer = None

    def _import_layer(self, layer_dotted_name):
        parts = layer_dotted_name.split('.')
        if len(parts) < 2:
            raise ValueError('no dot in layer dotted name')
        module_name = '.'.join(parts[:-1])
        layer_name = parts[-1]
        __import__(module_name)
        module = sys.modules[module_name]
        layer = getattr(module, layer_name)
        return layer

    def _get_layer(self):
        return self.zope_layer

    def start_zope_server(self, layer_dotted_name):
        new_layer = self._import_layer(layer_dotted_name)
        if self.zope_layer and self.zope_layer is not new_layer:
            self.stop_zope_server()
        setup_layer(new_layer)
        self.zope_layer = new_layer

    def stop_zope_server(self):
        tear_down()
        self.zope_layer = None

    def zodb_setup(self):
        from zope.testing.testrunner.runner import order_by_bases
        layers = order_by_bases([self.zope_layer])
        for layer in layers:
            if hasattr(layer, 'testSetUp'):
                layer.testSetUp()

    def zodb_teardown(self):
        from zope.testing.testrunner.runner import order_by_bases
        layers = order_by_bases([self.zope_layer])
        layers.reverse()
        for layer in layers:
            if hasattr(layer, 'testTearDown'):
                layer.testTearDown()


setup_layers = {}


def setup_layer(layer, setup_layers=setup_layers):
    assert layer is not object
    if layer not in setup_layers:
        for base in layer.__bases__:
            if base is not object:
                setup_layer(base, setup_layers)
        if hasattr(layer, 'setUp'):
            layer.setUp()
        setup_layers[layer] = 1


def tear_down(setup_layers=setup_layers):
    from zope.testing.testrunner.runner import order_by_bases
    # Tear down any layers not needed for these tests. The unneeded layers
    # might interfere.
    unneeded = [l for l in setup_layers]
    unneeded = order_by_bases(unneeded)
    unneeded.reverse()
    for l in unneeded:
        try:
            try:
                if hasattr(l, 'tearDown'):
                    l.tearDown()
            except NotImplementedError:
                pass
        finally:
            del setup_layers[l]
