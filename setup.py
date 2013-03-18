from setuptools import setup
from setuptools import find_packages

version = '0.1.0'

long_description = (
    open('README.rst').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.txt').read()
    + '\n' +
    open('CHANGES.txt').read()
    + '\n')


console_scripts = [
    "act_server = plone.app.robotframework.server:server",  # BBB
    "robot-server = plone.app.robotframework.server:server",
    "pybot = plone.app.robotframework.robotentrypoints:pybot",
    "rebot = plone.app.robotframework.robotentrypoints:rebot",
]

entry_points = dict(console_scripts=console_scripts)

setup(name='plone.app.robotframework',
      version=version,
      description="Robot Framework testing resources for Plone",
      long_description=long_description,
      classifiers=[
          "Programming Language :: Python",
      ],
      keywords='',
      author='',
      author_email='',
      url='https://github.com/plone/plone.act/',
      license='gpl',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['plone', 'plone.app'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'argparse',
          'plone.app.testing[robot]>=4.2.2',
          'zope.deprecation',
      ],
      extras_require={'reload': [
          'watchdog'
      ]},
      entry_points=entry_points,
      )
