import unittest2 as unittest

from Products.CMFCore.utils import getToolByName

from vnccollab.portal.testing import \
    VNCCOLLAB_PORTAL_INTEGRATION_TESTING


class TestInstalled(unittest.TestCase):

    layer = VNCCOLLAB_PORTAL_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.qi_tool = getToolByName(self.portal, 'portal_quickinstaller')

    def test_product_is_installed(self):
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
