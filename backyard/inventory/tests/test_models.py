"""backyard.inventory.tests.test_models"""
from django.test import TransactionTestCase
from django.db import IntegrityError
from backyard.inventory.models import Maker


class MakerTransactionTest(TransactionTestCase):
    """transaction test of Maker."""

    def test_create(self):
        """create."""
        maker_name = 'someone maker'
        query = Maker(name=maker_name)
        query.save()
        self.assertEqual(query.__str__(), maker_name)

    def test_create_fail(self):
        """create."""
        maker_name = 'someone maker'
        query = Maker(name=maker_name)
        query.save()
        query = Maker(name=maker_name)
        with self.assertRaises(IntegrityError):
            query.save()
