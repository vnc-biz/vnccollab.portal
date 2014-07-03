from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.testing import z2

from zope.configuration import xmlconfig


class VnccollabPortalLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import vnccollab.portal
        xmlconfig.file(
            'configure.zcml',
            vnccollab.portal,
            context=configurationContext
        )

        # Install products that use an old-style initialize() function
        #z2.installProduct(app, 'Products.PloneFormGen')

#    def tearDownZope(self, app):
#        # Uninstall products installed above
#        z2.uninstallProduct(app, 'Products.PloneFormGen')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'vnccollab.portal:default')

VNCCOLLAB_PORTAL_FIXTURE = VnccollabPortalLayer()

VNCCOLLAB_PORTAL_INTEGRATION_TESTING = IntegrationTesting(
    bases=(VNCCOLLAB_PORTAL_FIXTURE,),
    name="VnccollabPortalLayer:Integration"
)
VNCCOLLAB_PORTAL_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(VNCCOLLAB_PORTAL_FIXTURE, z2.ZSERVER_FIXTURE),
    name="VnccollabPortalLayer:Functional"
)
