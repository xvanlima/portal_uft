"""Setup tests for this package."""
from kitconcept import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from portal_uft.testing import PORTAL_UFT_INTEGRATION_TESTING  # noqa: E501
from Products.CMFPlone.utils import get_installer

import unittest


class TestSetup(unittest.TestCase):
    """Test that portal_uft is properly installed."""

    layer = PORTAL_UFT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.setup = self.portal.portal_setup
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_product_installed(self):
        """Test if portal_uft is installed."""
        self.assertTrue(self.installer.is_product_installed("portal_uft"))

    def test_browserlayer(self):
        """Test that IPORTAL_UFTLayer is registered."""
        from plone.browserlayer import utils
        from portal_uft.interfaces import IPORTAL_UFTLayer

        self.assertIn(IPORTAL_UFTLayer, utils.registered_layers())

    def test_latest_version(self):
        """Test latest version of default profile."""
        self.assertEqual(
            self.setup.getLastVersionForProfile("portal_uft:default")[0],
            "20220623003",
        )


class TestUninstall(unittest.TestCase):

    layer = PORTAL_UFT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("portal_uft")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if portal_uft is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed("portal_uft"))

    def test_browserlayer_removed(self):
        """Test that IPORTAL_UFTLayer is removed."""
        from plone.browserlayer import utils
        from portal_uft.interfaces import IPORTAL_UFTLayer

        self.assertNotIn(IPORTAL_UFTLayer, utils.registered_layers())
