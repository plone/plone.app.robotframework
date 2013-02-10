from setuptools import setup, find_packages

version = '0.1'

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
    "act_server = plone.act.server:server",
    "pybot = plone.act.robotentrypoints:pybot",
    "rebot = plone.act.robotentrypoints:rebot",
]

entry_points = dict(console_scripts=console_scripts)

setup(name='plone.act',
      version=version,
      description="Acceptance testing for Plone",
      long_description=long_description,
      classifiers=[
          "Programming Language :: Python",
      ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='gpl',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['plone'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.app.testing[robot]>=4.2.2',
      ],
      entry_points=entry_points,
      )
