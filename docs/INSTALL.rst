vnccollab.portal Installation
-----------------------------

The preferred way to install vnccolla.portal is using zc.buildout, mr.developer
and the plone.recipe.zope2instance recipe to manage your project, you can do
this:

* Add the following to your buildout.cfg file: ::

    [buildout]
    ...
    eggs =
        ...
        pyzimbra
        vnccollab.portal

    extensions +=
        mr.developer

    auto-checkout =
        pyzimbra

    [instance]
    zcml =
        ${buildout:eggs}
        ...
        vnccollab.portal-overrides

    [sources]
    # we are currently using our fork of pyzimbra
    pyzimbra = git git://github.com/vnc-biz/pyzimbra.git branch=master

    [versions]
    collective.js.jqueryui = 1.8.16.8
    plone.app.jquery = 1.7.2
    plone.app.jquerytools = 1.4



* Re-run buildout, e.g. with: ::

    $ ./bin/buildout

You can skip the ZCML slugs if you are going to explicitly include the packages
from another package's configure.zcml file.
