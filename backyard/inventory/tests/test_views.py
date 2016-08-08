# -*- coding: utf-8 -*-
"""backyard.inventory.tests.test_views."""
from django.test import TestCase, Client


class ViewTest(TestCase):
    """views unit tests."""
    fixtures = ['backyard/inventory/tests/data/users.json']

    def setUp(self):
        """initialize."""
        self.client = Client()
        self.username = 'toshihisa'
        self.correct_password = 'phie1aeRei'
        self.incorrect_password = 'hogehoge'

    def test_login(self):
        """login test."""
        resp = self.client.post('/login', {'username': self.username,
                                           'password': self.correct_password})
        self.assertEqual(resp.status_code, 200)
