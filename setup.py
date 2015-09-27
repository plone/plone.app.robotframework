from setuptools import setup
from setuptools import find_packages

version = '0.9.12'


def indented(filename):
    return ''.join([indent(line) for line in open(filename)])


def indent(line):
    return '   ' + line


long_description = (
    open('README.rst').read()
    + '\n' +
    indented('versions.cfg')
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.txt').read()
    + '\n' +
    open('CHANGES.txt').read()
    + '\n'
)


console_scripts = [
    "robot-server = plone.app.robotframework.server:server",
    "robot = plone.app.robotframework.robotentrypoints:robot",
    "robot-debug = plone.app.robotframework.robotentrypoints:robot_debug",
    "pybot = plone.app.robotframework.robotentrypoints:pybot",
    "ride = plone.app.robotframework.robotentrypoints:ride",
    "libdoc = plone.app.robotframework.robotentrypoints:libdoc",
    "pybabel = plone.app.robotframework.robotentrypoints:pybabel",
]

entry_points = dict(console_scripts=console_scripts)

install_requires = [
    'Products.CMFCore',
    'Products.CMFPlone',
    'Products.MailHost',
    'Products.PlonePAS',
    'Products.PluggableAuthService',
    'argparse',
    'babel',
    'decorator',   # required by r.selenium2library on Python 2.6.x
    'five.globalrequest',
    'plone.app.testing',
    'plone.testing',
    'plone.uuid',
    'robotframework',
    'robotframework-selenium2library',
    'robotsuite',  # not a direct dependency, but required for convenience
    'selenium',
    'setuptools',
    'simplejson',  # required for SauceLabs-keywords on Python 2.6.x
    'zope.component',
    'zope.configuration',
    'zope.i18n',
    'zope.schema',
    'zope.testing',
]

test_requires = [
    'plone.app.dexterity',
    'plone.app.textfield',
    'plone.dexterity',
    'robotsuite',
    'z3c.form',
]

debug_requires = [
    # REPL-debugger for Robot Framework:
    'robotframework-debuglibrary',
]

ride_requires = [
    # Robot Framework IDE:
    'robotframework-ride'
]

speak_requires = [
    # Enable talking screen casts:
    'collective.js.speakjs'
]

reload_requires = [
    # Watch for filesystem changes:
    'watchdog'
]

docs_requires = [
    # Include robot-files outside docs:
    'sphinxcontrib-robotdoc'
]

setup(
    name='plone.app.robotframework',
    version=version,
    description="Robot Framework testing resources for Plone",
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
    keywords='',
    author='Asko Soukka',
    author_email='asko.soukka@iki.fi',
    url='https://github.com/plone/plone.app.robotframework/',
    license='gpl',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['plone', 'plone.app'],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    extras_require={'ride': ride_requires,
                    'speak': speak_requires,
                    'test': test_requires,
                    'reload': reload_requires,
                    'docs': docs_requires,
                    'debug': debug_requires},
    entry_points=entry_points,
)
