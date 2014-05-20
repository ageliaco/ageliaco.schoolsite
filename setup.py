from setuptools import setup, find_packages

version = '1.0b5'

setup(name='ageliaco.schoolsite',
      version=version,
      description="",
      #long_description=open("README.rst").read() + "\n" +
      #                 open("CHANGES.rst").read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
          "Framework :: Plone",
          "Programming Language :: Python",
      ],
      keywords='plone content dexterity',
      author='Kamon Ayeva',
      author_email='',
      url='https://github.com/kamon/ageliaco.schoolsite',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ageliaco',],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.CMFPlone',
          'plone.app.contenttypes[atrefs]',
          'collective.fontawesome',
          'collective.js.datatables',
          #'z3c.jbot', 
      ],
      extras_require={
          'test': [
          ],
      },
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
