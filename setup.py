import os

from setuptools import setup, find_packages

README = ""
CHANGES = ""

requires = [
    "zope.interface"
    ]

sqlalchemy_requires = [
    "sqlalchemy", 
    "sqlahelper"
]

setup(name='spectacles',
      version='0.0',
      description='lookup sqlalchemy-models relations',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        ],
      author='',
      author_email='',
      url='',
      packages=find_packages(),
      install_requires = requires,
      extras_require = {"sqlalchemy": sqlalchemy_requires}, 
      entry_points = {
        "console_scripts": (
            "spectacles = spectacles.scripts:main", 
            )
        },
      )
