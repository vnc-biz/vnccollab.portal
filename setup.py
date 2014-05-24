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
      author='Jose Dinuncio',
      author_email='jose.dinuncio@vnc.biz',
      url='https://github.com/vnc-biz/vnccollab.portal',
      license='gpl',
      packages=find_packages(),
      namespace_packages=['vnccollab', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Plone',
          'Pillow',
          'plone.api',
          'plone.app.iterate',
          'plone.app.workflow',
          'plone.app.workflowmanager',
          'Products.PloneKeywordManager',
          'collective.imageinbox',
          'collective.bulksharing',
          'collective.vaporisation',
          'collective.documentviewer',
          'collective.externaleditor',
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
