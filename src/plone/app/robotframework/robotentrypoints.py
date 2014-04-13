import sys

from robot import run_cli
from robot import libdoc as ld

import pkg_resources

try:
    pkg_resources.get_distribution('robotframework-ride')
except pkg_resources.DistributionNotFound:
    HAS_RIDE = False
else:
    HAS_RIDE = True


def pybot():
    # This code hides warnings for known Sphinx-only-directives when
    # executing pybot against Sphinx-documentation:
    from docutils.parsers.rst.directives import register_directive
    from docutils.parsers.rst.roles import register_local_role
    dummy_directive = lambda *args: []
    options = ('maxdepth', 'creates', 'numbered', 'hidden')
    setattr(dummy_directive, 'content', True)
    setattr(dummy_directive, 'options', dict([(opt, str) for opt in options]))
    register_directive('toctree', dummy_directive)
    register_directive('robotframework', dummy_directive)
    register_local_role('ref', dummy_directive)

    # Run pybot
    run_cli(sys.argv[1:])


def robot():
    run_cli(['--listener', 'plone.app.robotframework.RobotListener']
            + sys.argv[1:])


def robot_debug():
    run_cli(['--listener', 'plone.app.robotframework.RobotListener',
             '-v', 'SELENIUM_RUN_ON_FAILURE:Debug']
            + sys.argv[1:])


def ride():
    if HAS_RIDE:
        from robotide import main
        main(*sys.argv[1:])
    else:
        print u"""\
Package robotframework-ride was not found. Please, install
plone.app.robotframework with proper extras, like:

    plone.app.robotframework[ride]

or

    plone.app.robotframework[ride,reload]

Remember that ride must be lauched with system python with
wxPython installed, like:

    /usr/bin/python bin/ride
"""


def libdoc():
    ld.libdoc_cli(sys.argv[1:])


def pybabel():
    # This registers our minimal robot translation extractor
    import babel.messages.extract
    babel.messages.extract.DEFAULT_MAPPING.extend([
        ('**.rst', 'plone.app.robotframework.pybabel:extract_robot'),
        ('**.robot', 'plone.app.robotframework.pybabel:extract_robot')
    ])

    # This code hides warnings for known Sphinx-only-directives when
    # executing pybot against Sphinx-documentation:
    from docutils.parsers.rst.directives import register_directive
    from docutils.parsers.rst.roles import register_local_role
    dummy_directive = lambda *args: []
    options = ('maxdepth', 'creates', 'numbered', 'hidden')
    setattr(dummy_directive, 'content', True)
    setattr(dummy_directive, 'options', dict([(opt, str) for opt in options]))
    register_directive('toctree', dummy_directive)
    register_directive('robotframework', dummy_directive)
    register_local_role('ref', dummy_directive)

    from babel.messages.frontend import main
    main()
