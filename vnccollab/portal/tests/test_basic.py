import unittest2 as unittest

from Products.CMFCore.utils import getToolByName
from plone.app.controlpanel.security import SecurityControlPanelAdapter

from vnccollab.portal.testing import \
    VNCCOLLAB_PORTAL_INTEGRATION_TESTING


class TestInstalled(unittest.TestCase):

    layer = VNCCOLLAB_PORTAL_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.qi_tool = getToolByName(self.portal, 'portal_quickinstaller')

    def test_products_are_installed(self):
        """ Validate that our products GS profile has been run and the product
            installed
        """
        addons = ['vnccollab.portal', 'vnccollab.common',
                  'vnccollab.content', 'vnccollab.theme',
                  'vnccollab.redmine', 'vnccollab.zimbra']

        for pid in addons:
            installed = [p['id'] for p in self.qi_tool.listInstalledProducts()]
            self.assertTrue(pid in installed,
                            'package "%s" appears not to have been installed'
                            % pid)

    def test_default_page_removed(self):
        """Verifies that the default page property has been removed."""
        self.assertFalse(self.portal.hasProperty('default_page'))

    def test_self_registration_disabled(self):
        """Verifiies that self registration is disabled."""
        schema = SecurityControlPanelAdapter(self.portal)
        self.assertFalse(schema.enable_self_reg)

    def test_user_folders_enabled(self):
        """Verifiies that user folders are enabled."""
        schema = SecurityControlPanelAdapter(self.portal)
        self.assertTrue(schema.enable_user_folders)

    def test_dashboard_exists(self):
        """Verifies that dashboard was created."""
        self.assertTrue('dashboard' in self.portal)
