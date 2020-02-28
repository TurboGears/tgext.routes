from setuptools import setup, find_packages
import os

version = '0.2.1'

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
except IOError:
    README = ''

TEST_REQUIREMENTS = [
  'pytest',
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
      author_email='amol@turbogears.org',
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
           'testing': TEST_REQUIREMENTS,
      },
      tests_require=TEST_REQUIREMENTS,
      entry_points="""
      # -*- Entry points: -*-
      """)
