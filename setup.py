from setuptools import find_packages
from setuptools import setup

import sys

version = '2.0.0a1'


def indented(filename):
    return ''.join([indent(line) for line in open(filename)])


def indent(line):
    return '   ' + line


def read(filename):
    with open(filename) as myfile:
        try:
            return myfile.read()
        except UnicodeDecodeError:
            # Happens on one Jenkins node on Python 3.6,
            # so maybe it happens for users too.
            pass
    # Opening and reading as text failed, so retry opening as bytes.
    with open(filename, "rb") as myfile:
        contents = myfile.read()
        return contents.decode("utf-8")


long_description = (
    read('README.rst') +
    '\n' +
    'Contributors\n'
    '============\n' +
    '\n' +
    read('CONTRIBUTORS.rst') +
    '\n' +
    read('CHANGES.rst')
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
    'Products.PlonePAS >= 5.0.1',
    'Products.PluggableAuthService',
    'babel',
    'plone.app.testing',
    'plone.testing',
    'plone.uuid',
    'robotframework',
    'robotframework-selenium2library',
    'robotsuite',  # not a direct dependency, but required for convenience
    'selenium',
    'setuptools',
    'six',
    'zope.component',
    'zope.configuration',
    'zope.i18n',
    'zope.schema',
    'zope.testrunner',
]

if sys.version_info < (2, 7):
    install_requires.extend([
        'argparse',
        'decorator',   # required by r.selenium2library on Python 2.6.x
        'simplejson',  # required for SauceLabs-keywords on Python 2.6.x
    ])

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
        "Development Status :: 5 - Production/Stable",
        "Framework :: Plone",
        "Framework :: Plone :: 6.0",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords='robot automatic browser testing Plone',
    author='Asko Soukka',
    author_email='asko.soukka@iki.fi',
    url='https://github.com/plone/plone.app.robotframework/',
    license='GPL',
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
