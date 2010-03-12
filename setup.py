from setuptools import setup, find_packages
import sys, os

version = '2.0'
shortdesc ="Image field and/or patch with clipping support for Plone/Archetypes."
longdesc = open(os.path.join(os.path.dirname(__file__), 'README.txt')).read()
longdesc += open(os.path.join(os.path.dirname(__file__), 'LICENSE.txt')).read()

setup(name='archetypes.clippingimage',
      version=version,
      description=shortdesc,
      long_description=longdesc,
      classifiers=[
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Framework :: Zope2',
            'Framework :: Plone',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Libraries :: Python Modules'
      ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Jens Klein',
      author_email='jens@bluedynamics.com',
      url='https://svn.plone.org/svn/archetypes/MoreFieldsAndWidgets/archetypes.clippingimage',
      license='BSD',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['archetypes',],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.Archetypes',
          'collective.monkeypatcher',
          # -*- Extra requirements: -*
      ],
      )
