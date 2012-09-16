import sys


class PloneLibrary(object):
    def get_site_owner_name(self):
        """*DEPRECATED* Instead use Robot Framework's variable files
        to directly pull in p.a.testing.interfaces.
        See plone.act/acceptance-tests/rf_variable_file.txt and
        http://robotframework.googlecode.com/hg/doc/userguide/RobotFrameworkUserGuide.html?r=2.7.1#resource-and-variable-files
        """
        import plone.app.testing
        return plone.app.testing.interfaces.SITE_OWNER_NAME

    def get_site_owner_password(self):
        """*DEPRECATED* Instead use Robot Framework's variable files
        to directly pull in p.a.testing.interfaces.
        See plone.act/acceptance-tests/rf_variable_file.txt and
        http://robotframework.googlecode.com/hg/doc/userguide/RobotFrameworkUserGuide.html?r=2.7.1#resource-and-variable-files
        """
        import plone.app.testing
        return plone.app.testing.interfaces.SITE_OWNER_PASSWORD

    def stop_for_debugging(self):
        for attr in ('stdin', 'stdout', 'stderr'):
            setattr(sys, attr, getattr(sys, '__%s__' % attr))
        import pdb; pdb.set_trace()


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
        #global zope_layer
        new_layer = self._import_layer(layer_dotted_name)
        if self.zope_layer and self.zope_layer is not new_layer:
            self.stop_zope_server()
        setup_layer(new_layer)
        self.zope_layer = new_layer

    def stop_zope_server(self):
        tear_down()
        #global zope_layer
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

    def apply_profile(self, profile_name):
        from plone.app.testing import applyProfile
        applyProfile(self.zope_layer['portal'],profile_name)

#zope_layer = None
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
