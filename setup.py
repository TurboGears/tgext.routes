from setuptools import setup, find_packages
import os

version = '0.1.0'

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
except IOError:
    README = ''

TEST_REQUIREMENTS = [
  'nose',
  'webtest',
]

setup(name='tgext.routes',
      version=version,
      description="Routes based dispatching for TurboGears2",
      long_description=README,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Environment :: Web Environment",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: TurboGears"
        ],
      keywords='turbogears2.extension',
      author='Alessandro Molina',
      author_email='alessandro.molina@axant.it',
      url='https://github.com/TurboGears/tgext.routes',
      license='MIT',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['tgext'],
      include_package_data=True,
      package_data = {'':['*.html', '*.js', '*.css', '*.png', '*.gif']},
      zip_safe=False,
      install_requires=[
        "TurboGears2 >= 2.3.8",
        "routes"
      ],
      extras_require={
           # Used by Travis and Coverage due to setup.py nosetests
           # causing a coredump when used with coverage
           'testing': TEST_REQUIREMENTS,
      },
      test_suite='nose.collector',
      tests_require=TEST_REQUIREMENTS,
      entry_points="""
      # -*- Entry points: -*-
      """)
