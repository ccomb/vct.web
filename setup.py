import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

setup(name='vct.demo',
      version='0.1',
      description='First demo for Virtual Care Team',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        ],
      author='',
      author_email='',
      url='',
      keywords='',
      packages=find_packages(),
      namespace_packages = ['vct'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
            'couchdbkit',
            ],
      tests_require=[
            ],
      test_suite="",
      entry_points = """
      """
      )

