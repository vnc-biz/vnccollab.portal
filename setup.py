from setuptools import setup, find_packages
import os

version = open('version.txt').readline().strip()

long_description = (
    open('README.rst').read()
    + '\n' +
    open(os.path.join("docs", "HISTORY.txt")).read())

setup(name='vnccollab.portal',
      version=version,
      description="VNC Collaboration Portal",
      long_description=long_description,
      classifiers=[
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.6",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='gpl',
      packages=find_packages(),
      namespace_packages=['vnccollab', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.api',
          'vnccollab.common',
          'vnccollab.content',
          'vnccollab.redmine',
          'vnccollab.zimbra',
          'vnccollab.theme',
      ],
      extras_require={'test': ['plone.app.testing[robot]>=4.2.2']},
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
