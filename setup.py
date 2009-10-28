import os
import sys

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'setuptools',
    'repoze.bfg',
    'SQLAlchemy',
    'transaction',
    'repoze.tm2',
    'zope.sqlalchemy',
    'couchdbkit',
    'PasteDeploy',
    ]

if sys.version_info[:3] < (2,5,0):
    requires.append('pysqlite')

setup(name='vct.demo',
      version='0.1',
      description='vct.demo',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg zope',
      packages=find_packages(),
      namespace_packages = ['vct'],
      include_package_data=True,
      zip_safe=False,
      test_suite='vct.demo',
      install_requires = requires,
      entry_points = """\
      [paste.app_factory]
      app = vct.demo.run:app
      """
      )

