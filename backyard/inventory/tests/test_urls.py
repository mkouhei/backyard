"""backayrd.inventory.tests.test_urls."""
import unittest
from django.core.urlresolvers import resolve, Resolver404


class TestUrls(unittest.TestCase):
    """urls test."""

    def test_urls(self):
        """test urls."""
        self.assertEqual(resolve('/admin').view_name, 'admin:index')
        self.assertEqual(resolve('/login').view_name,
                         'django.contrib.auth.views.login')
        self.assertEqual(resolve('/logout').view_name,
                         'django.contrib.auth.views.logout')
        self.assertEqual(resolve('/').view_name,
                         'backyard.inventory.views.dashboard.DashboardView')

    def test_not_found(self):
        """not found."""
        with self.assertRaises(Resolver404):
            resolve('')
