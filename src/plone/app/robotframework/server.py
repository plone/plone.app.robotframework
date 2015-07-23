# -*- coding: utf-8 -*-
import argparse
import logging
import select
import os
import sys
import time
import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer

import pkg_resources

try:
    pkg_resources.get_distribution('watchdog')
except pkg_resources.DistributionNotFound:
    HAS_RELOAD = False
else:
    from plone.app.robotframework.reload import ForkLoop
    from plone.app.robotframework.reload import Watcher
    HAS_RELOAD = True

from plone.app.robotframework.remote import RemoteLibrary

HAS_DEBUG_MODE = False
HAS_VERBOSE_CONSOLE = False

ZSERVER_HOST = os.getenv("ZSERVER_HOST", "localhost")
LISTENER_HOST = os.getenv("LISTENER_HOST", ZSERVER_HOST)
LISTENER_PORT = int(os.getenv("LISTENER_PORT", 49999))

TIME = lambda: time.strftime('%H:%M:%S')
WAIT = lambda msg:  '{0} [\033[33m wait \033[0m] {1}'.format(TIME(), msg)
ERROR = lambda msg: '{0} [\033[31m ERROR \033[0m] {1}'.format(TIME(), msg)
READY = lambda msg: '{0} [\033[32m ready \033[0m] {1}'.format(TIME(), msg)


def start(zope_layer_dotted_name):

    print WAIT("Starting Zope 2 server")

    zsl = Zope2Server()
    zsl.start_zope_server(zope_layer_dotted_name)

    print READY("Started Zope 2 server")

    listener = SimpleXMLRPCServer((LISTENER_HOST, LISTENER_PORT),
                                  logRequests=False)
    listener.allow_none = True
    listener.register_function(zsl.zodb_setup, 'zodb_setup')
    listener.register_function(zsl.zodb_teardown, 'zodb_teardown')

    try:
        listener.serve_forever()
    finally:
        print
        print WAIT("Stopping Zope 2 server")

        zsl.stop_zope_server()

        print READY("Zope 2 server stopped")


def start_reload(zope_layer_dotted_name, reload_paths=('src',),
                 preload_layer_dotted_name='plone.app.testing.PLONE_FIXTURE',
                 extensions=None):

    print WAIT("Starting Zope 2 server")

    zsl = Zope2Server()
    zsl.start_zope_server(preload_layer_dotted_name)

    forkloop = ForkLoop()
    watcher = Watcher(reload_paths, forkloop)
    if extensions:
        watcher.allowed_extensions = extensions
    elif HAS_DEBUG_MODE:
        watcher.allowed_extensions.remove('pt')
    watcher.start()
    forkloop.start()

    if forkloop.exit:
        print WAIT("Stopping Zope 2 server")
        zsl.stop_zope_server()
        print READY("Zope 2 server stopped")
        return

    # XXX: For unknown reason call to socket.gethostbyaddr may cause malloc
    # errors on OSX in forked child when called from medusa http_server, but
    # proper sleep seem to fix it:
    import time
    import socket
    import platform
    if 'Darwin' in platform.uname():
        gethostbyaddr = socket.gethostbyaddr
        socket.gethostbyaddr = lambda x: time.sleep(0.5) or (ZSERVER_HOST,)

    # Setting smaller asyncore poll timeout will speed up restart a bit
    import plone.testing.z2
    plone.testing.z2.ZServer.timeout = 0.5

    zsl.amend_zope_server(zope_layer_dotted_name)

    if HAS_DEBUG_MODE:
        import App.config
        config = App.config.getConfiguration()
        config.debug_mode = HAS_DEBUG_MODE
        App.config.setConfiguration(config)

    if 'Darwin' in platform.uname():
        socket.gethostbyaddr = gethostbyaddr

    print READY("Zope 2 server started")

    try:
        listener = SimpleXMLRPCServer((LISTENER_HOST, LISTENER_PORT),
                                      logRequests=False)
    except socket.error as e:
        print ERROR(str(e))
        print WAIT("Pruning Zope 2 server")
        zsl.prune_zope_server()
        return

    listener.timeout = 0.5
    listener.allow_none = True
    listener.register_function(zsl.zodb_setup, 'zodb_setup')
    listener.register_function(zsl.zodb_teardown, 'zodb_teardown')

    try:
        while not forkloop.exit:
            listener.handle_request()
    except select.error:  # Interrupted system call
        pass
    finally:
        print WAIT("Pruning Zope 2 server")
        zsl.prune_zope_server()


def server():
    if HAS_RELOAD:
        parser = argparse.ArgumentParser()
    else:
        parser = argparse.ArgumentParser(
            epilog='Note: require \'plone.app.robotframework\' with '
                   '\'[reload]\'-extras to get the automatic code reloading '
                   'support (powered by \'watchdog\').')
    parser.add_argument('layer')
    parser.add_argument('--debug-mode', '-d', dest='debug_mode',
                        action='store_true')
    VERBOSE_HELP = (
        '-v information about test layers setup and tear down, '
        '-vv add logging.WARNING messages, '
        '-vvv add INFO messages, -vvvv add DEBUG messages.')
    parser.add_argument('--verbose', '-v', action='count', help=VERBOSE_HELP)

    if HAS_RELOAD:
        parser.add_argument('--reload-path', '-p', dest='reload_paths',
                            action='append')
        parser.add_argument('--reload-extensions', '-x', dest='extensions',
                            nargs='*', help=(
                                'file extensions to watch for changes'))
        parser.add_argument('--preload-layer', '-l', dest='preload_layer')
        parser.add_argument('--no-reload', '-n', dest='reload',
                            action='store_false')
    args = parser.parse_args()

    # Set debug mode
    if args.debug_mode is True:
        global HAS_DEBUG_MODE
        HAS_DEBUG_MODE = True

    # Set console log level
    if args.verbose:
        global HAS_VERBOSE_CONSOLE
        HAS_VERBOSE_CONSOLE = True
        loglevel = logging.ERROR - (args.verbose - 1) * 10
    else:
        loglevel = logging.ERROR
    logging.basicConfig(level=loglevel)

    # Set reload when available
    if not HAS_RELOAD or args.reload is False:
        try:
            start(args.layer)
        except KeyboardInterrupt:
            pass
    else:
        start_reload(args.layer, args.reload_paths or ['src'],
                     args.preload_layer or 'plone.app.testing.PLONE_FIXTURE',
                     args.extensions)


class RobotListener:

    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        server_listener_address = 'http://%s:%s' % (
            LISTENER_HOST, LISTENER_PORT)
        self.server = xmlrpclib.ServerProxy(server_listener_address)

    def start_test(self, name, attrs):
        self.server.zodb_setup()

    def end_test(self, name, attrs):
        self.server.zodb_teardown()

ZODB = RobotListener  # BBB


class Zope2Server:

    def __init__(self):
        self.zope_layer = None
        self.extra_layers = {}

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

    def start_zope_server(self, layer_dotted_name):
        new_layer = self._import_layer(layer_dotted_name)
        if self.zope_layer and self.zope_layer is not new_layer:
            self.stop_zope_server()
        setup_layer(new_layer)
        self.zope_layer = new_layer

    def set_zope_layer(self, layer_dotted_name):
        """Explicitly set the current Zope layer, when you know what you are
        doing
        """
        new_layer = self._import_layer(layer_dotted_name)
        self.zope_layer = new_layer

    def amend_zope_server(self, layer_dotted_name):
        """Set up extra layers up to given layer_dotted_name"""
        old_layers = setup_layers.copy()
        new_layer = self._import_layer(layer_dotted_name)
        setup_layer(new_layer)
        for key in setup_layers.keys():
            if key not in old_layers:
                self.extra_layers[key] = 1
        self.zope_layer = new_layer

    def prune_zope_server(self):
        """Tear down the last set of layers set up with amend_zope_server"""
        tear_down(self.extra_layers)
        self.extra_layers = {}
        self.zope_layer = None

    def stop_zope_server(self):
        tear_down()
        self.zope_layer = None

    def zodb_setup(self, layer_dotted_name=None):
        if layer_dotted_name:
            self.set_zope_layer(layer_dotted_name)

        from zope.testing.testrunner.runner import order_by_bases
        layers = order_by_bases([self.zope_layer])
        for layer in layers:
            if hasattr(layer, 'testSetUp'):
                if HAS_VERBOSE_CONSOLE:
                    print WAIT("Test set up {0}.{1}".format(
                        layer.__module__, layer.__name__))
                layer.testSetUp()
        if HAS_VERBOSE_CONSOLE:
            print READY("Test set up")

    def zodb_teardown(self, layer_dotted_name=None):
        if layer_dotted_name:
            self.set_zope_layer(layer_dotted_name)

        from zope.testing.testrunner.runner import order_by_bases
        layers = order_by_bases([self.zope_layer])
        layers.reverse()
        for layer in layers:
            if hasattr(layer, 'testTearDown'):
                if HAS_VERBOSE_CONSOLE:
                    print WAIT("Test tear down {0}.{1}".format(
                        layer.__module__, layer.__name__))
                layer.testTearDown()
        if HAS_VERBOSE_CONSOLE:
            print READY("Test torn down")


setup_layers = {}


def setup_layer(layer, setup_layers=setup_layers):
    assert layer is not object
    if layer not in setup_layers:
        for base in layer.__bases__:
            if base is not object:
                setup_layer(base, setup_layers)
        if hasattr(layer, 'setUp'):
            name = "{0}.{1}".format(layer.__module__, layer.__name__)
            if HAS_VERBOSE_CONSOLE and name == 'plone.testing.z2.Startup':
                print WAIT("Set up {0}.{1} (debug-mode={2})".format(
                    layer.__module__, layer.__name__, HAS_DEBUG_MODE))
            elif HAS_VERBOSE_CONSOLE:
                print WAIT("Set up {0}.{1}".format(layer.__module__,
                                                   layer.__name__))
            layer.setUp()
            if HAS_DEBUG_MODE and name == 'plone.testing.z2.Startup':
                import App.config
                config = App.config.getConfiguration()
                config.debug_mode = HAS_DEBUG_MODE
                App.config.setConfiguration(config)
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
                    if HAS_VERBOSE_CONSOLE:
                        print WAIT("Tear down {0}.{1}".format(l.__module__,
                                                              l.__name__))
                    l.tearDown()
            except NotImplementedError:
                pass
        finally:
            del setup_layers[l]


class Zope2ServerRemote(RemoteLibrary):
    """Provides ``remote_zodb_setup`` and ``remote_zodb_teardown`` -keywords to
    allow explicit test isolation via remote library calls when server is set
    up with robot-server and tests are run by a separate pybot process.

    *WARNING* These keywords does not with zope.testrunner (yet).
    """
    def remote_zodb_setup(self, layer_dotted_name):
        Zope2Server().zodb_setup(layer_dotted_name)

    def remote_zodb_teardown(self, layer_dotted_name):
        Zope2Server().zodb_teardown(layer_dotted_name)
